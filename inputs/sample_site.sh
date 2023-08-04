#! /bin/bash
python /home/svogt/repos/beep/scripts/launch_site_sampling.py --client-address 152.74.10.245:7778 \
     --cluster-name salen-OMe  \
     --cluster-collection initiators   \
     --sampling-molecule-name l-lactide \
     --sampling-molecule-collection monomers \
     --molecule-size 5 \
     --number-of-rounds 3 \
     --sampling-shell 3.0 \
     --zenith-angle 1.6 \
     --maximal-binding-sites 15 \
     --level-of-theory pbe0-d3_def2-svp \
     --refinement-level-of-theory pbe0-d3_def2-svp \
     --rmsd-value 0.15 \
     --program terachem \
     --sampling-tag tera \
     --noise \
     --purge 1.0 \
     #--username None \
     #--password None  \
     #--grid-size sparse
    # --keyword_id 1  \
    # --keyword_id_ref 2  \
    #--rmsd_symmetry
    #--level_of_theory upbe0-d3_def2-svp \

