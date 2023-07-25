#! /opt/anaconda/anaconda3/envs/geometric/bin/python

import qcfractal.interface as ptl
import qcelemental as qcel
import numpy as np
import sys
import qcengine
from pathlib import Path
from optparse import OptionParser
import json

usage ='''python %prog [options] scratch_dir output_file

A relaxed scan rutine with geomeTRIC, QCEngine and QCFractal
'''
parser = OptionParser(usage=usage)
parser.add_option("--client_address",
                  dest="client_address",
                  help="The URL address and port of the QCFractal server (default: localhost:7777)",
                  default="localhost:7777"
)
parser.add_option("--username",
                  dest="usern",
                  help="The username for the database client (Default = None)",
                  default=None
)
parser.add_option("--password",
                  dest="passwd",
                  help="The password for the database client (Default = None)",
                  default=None
)
parser.add_option("--starting-geometry",
                  dest="starting_geometry",
                  help="The QCFractal molecule id or the full path to a xyz file"
)
parser.add_option("--scan-coordinate",
                   dest="scan_coordinate",
                   help="The atomic coordinates to be scanned (e.g. 1 56 9)",
)
parser.add_option("--scan-type",
                   dest="scan_type",
                   help="The type of coordinate to scan (distance, angle, dihedral)",
)
parser.add_option("--base-name",
                   dest="base_name",
                   help="The name of the QCFractal Dataset where the optimized structures from the scan will be stored.",
)
parser.add_option("--scan-level-of-theory",
                   dest="scan_lot",
                   help="The level of theory of the optimization of the points along scan (Default: blyp-d3bj_def2_svp)",
                   default="blyp-d3bj_def2-svp",
)
parser.add_option("--energy-level-of-theory",
                   dest="energy_lot",
                  help="The level of theory of the energy single point for the optimized points along scan (Default: hf3c_minix)",
                   default="hf3c_minix",
)
parser.add_option("--initial-coordinate-value",
                   dest="initial_coordinate_value",
                   type = "float",
                   help="(Optional) The initial value of the coordiante to be scaned ",
                   default=0,
)
parser.add_option("--final-coordinate-value",
                   dest="final_coordinate_value",
                   type = "float",
                   help="The final value of the coordiante to be scaned ",
)
parser.add_option("--increment",
                   dest="increment",
                   type = "float",
                   help="The increment of the coordiante to be scaned (Can be negative)",
)
parser.add_option("--entry-rounding",
                   dest="entry_rounding",
                   type = "int",
                   help="The number of decimals to record  the index value of the scaned coordinate in the Dataset (Default: 1)",
                   default=1,
)
parser.add_option("--geometric-options",
                   dest="geometric_options",
                   help="A dictionary with options for the geomeTRIC program",
                   default="{}",
)
parser.add_option("--gradient-options",
                   dest="gradient_options",
                   help="A dictionary with options for the gradient computation",
                   default="{}",
)
parser.add_option("--program",
                   dest="program",
                  help="The program for the gradient computation (Default: terachem)",
                   default="terachem",
)
parser.add_option("--cores",
                   dest="ncores",
                   type = "int",
                  help="Number of computing cores or GPUs to use (Default: 1)",
                   default=1,
)
parser.add_option("--memory",
                   dest="memory",
                   type = "int",
                  help="Amount of memory to use in GB (Default: 16)",
                   default=16,
parser.add_option("--en_program",
                   dest="en_program",
                  help="The program for the energy computation (Default: psi4)",
                   default="psi4",
)
)
parser.add_option("--tag",
                  dest="tag",
                  help="The tag to used to specify the qcfractal-manager for the scan energy computation (default: refinement)",
                  default="refinement",
)
#parser.add_option("--output-file",
#                  dest="ofile",
#                  help="The name of the output file  (Default: out.dat)",
#                  default="out.dat",
#)

(options, args) = parser.parse_args()
scratch_dir, ofile = args

client_address = options.client_address
username = options.usern
password = options.passwd
start_geom =  options.starting_geometry
scan_coord_str = options.scan_coordinate
scan_type = options.scan_type  # "distance"
base_name = options.base_name  #"NH2CO+H2O->NH2CHO+OH"
lot_scan = options.scan_lot # 'blyp_6-31G'
lot_energy = options.energy_lot    # 'blyp_6-31G'#'hf3c_minix'
init_coord = options.initial_coordinate_value
end_coord = options.final_coordinate_value #1.10
step_size = options.increment #-0.05
geometric_options = json.loads(options.geometric_options)   #{}
gradient_options = json.loads(options.gradient_options)   #{}
gradient_program = options.program
energy_program = options.en_program
ncores = options.ncores
memory = options.memory
tag=options.tag
#ofile = options.ofile
entry_rounding = options.entry_rounding

client = ptl.FractalClient(address=client_address, verify=False, username=username, password=password)
scan_coord_list = [int(x) - 1 for x in scan_coord_str.split()]

def print_out(string):
    with open(ofile, "a") as f:
        f.write(string +'\n')


print_out('''
           ________  _______   ___       ________     ___    ___
          |\   __  \|\  ___ \ |\  \     |\   __  \   |\  \  /  /|
          \ \  \|\  \ \   __/|\ \  \    \ \  \|\  \  \ \  \/  / /
           \ \   _  _\ \  \_|/_\ \  \    \ \   __  \  \ \    / /
            \ \  \\  \\ \  \_|\ \ \  \____\ \  \ \  \  /     \/
             \ \__\\ _\\ \_______\ \_______\ \__\ \__\/  /\   \
              \|__|\|__|\|_______|\|_______|\|__|\|__/__/ /\ __\

Author: svogt 05/31/2022

          ''')

if len(start_geom.split('.')) > 1 :
    mol = qcel.models.Molecule.from_file(start_geom, orient=True)
else:
    mol = client.query_molecules(start_geom)[0]

scan_collection = base_name+'_'+lot_scan

for s in scan_coord_str.split():
    scan_collection += "_"+s

try:
    ds_scan = client.get_collection("Dataset", scan_collection)
except KeyError:
    ds_scan = ptl.collections.Dataset(scan_collection, client=client)

if not init_coord:
    if scan_type == 'distance':
        init_coord = mol.measure(scan_coord_list) * qcel.constants.conversion_factor("bohr", "angstrom")
    else:
        init_coord = mol.measure(scan_coord_list) 

coord_list = np.arange(init_coord, end_coord, step_size)

geometric_dict = {
                    "coordsys": "tric",
                    "maxiter": 100,
                    "program": gradient_program
                 }

geometric_dict.update(geometric_options)

method, basis = lot_scan.split("_")

geometric_task = {
        "schema_name": "qcschema_optimization_input",
        "schema_version": 1,
        "keywords": geometric_dict,
        "input_specification": {
                    "schema_name": "qcschema_input",
                    "schema_version": 1,
                    "driver": "gradient",
                    "model": {"method": method, "basis": basis},
                    "keywords": {},
                },
}

geometric_task['input_specification']['keywords'].update(gradient_options)

# Run computation
print_out('Initial molecule: {}'.format(mol))
print_out('Saving scan data in the QCFractal dataset named: {}'.format(scan_collection))
print_out('Will scan the coordinate {} from {} to {} with increments of {}'.format(scan_coord_str, init_coord, end_coord, step_size))

print_str = ''
for gparam in coord_list:
    entry_name = str(round(gparam,entry_rounding))
    df = ds_scan.get_entries()
    if entry_name in list(df.name):
        print_out("Entry {} has already been added, will continue to next step of the scan\n\n".format(entry_name))
        mol_id = int(df.loc[df['name'] == entry_name].molecule_id)
        mol = client.query_molecules(mol_id)[0]
        continue

    if scan_type == 'distance':
        constr_str = '''$set
        {} {} {}
        '''.format(scan_type, scan_coord_str, gparam)
    if scan_type == 'angle':
        constr_str = '''$set
        {} {} {}
        '''.format(scan_type, scan_coord_str, gparam)
    if scan_type == 'dihedral':
        constr_str = '''$set
        {} {} {}
        '''.format(scan_type, scan_coord_str, gparam)
    print_out('Setting {} spanned by atoms {} to {}\n'.format(scan_type, scan_coord_str, gparam))
    geometric_task["initial_molecule"] = mol
    geometric_task["keywords"]["constraints"] = constr_str
    print(geometric_task)

    print_out('Starting optimizitation at the {}/{} level of theory'.format(method, basis))
    ret = qcengine.compute_procedure(geometric_task, "geometric", local_options={"ncores": ncores, "memory" : memory, 'scratch_directory' : scratch_dir})
    print_out('Optimization finished! Will update the molecule now')
    print(ret)

    mol = ret.final_molecule

    print_out(''' 
          Final summary for this point:

          {}

          Final energy: {}

          Geometric output:

          {}

          '''.format(ret.final_molecule.to_string("xyz"), ret.energies[-1], ret.stdout)
    )
    print_out("Adding entry {} to the QCFractal Database collection {}".format(entry_name, scan_collection))
    try:
        ds_scan.add_entry(entry_name, mol)
        ds_scan.save()
    except KeyError:
        print_out("Initial molecule already exists")
        continue
    en_method, en_basis = lot_energy.split('_')
    print_out("Computing energy at the {}/{} level of theory".format(en_method, en_basis))
    ds_scan.compute(method = en_method, basis = en_basis, program = energy_program, tag=tag)


