/opt/shared/QCScan/relax.py  --client_address 152.74.10.245:7778 \
    --username ''\
    --password "" \
    --starting-geometry "38551" \
    --scan-coordinate "35 43" \
    --scan-type "distance" \
    --base-name "salen-OMe_d-lac_i1_0002" \
    --scan-level-of-theory "pbe0_def2-svp" \
    --energy-level-of-theory "pbe0-d3bj_def2-tzvp" \
    --initial-coordinate-value 0 \
    --final-coordinate-value 1.8 \
    --increment -0.05 \
    --entry-rounding 2 \
    --geometric-options '{"maxiter" : 150}' \
    --gradient-options '{"dftd": "d3"}' \
    --program "terachem" \
    --en_program "psi4" \
    --cores 1 \
    --memory 24 \
    --tag "rx_comp" \
    $1 \
    $2 \
