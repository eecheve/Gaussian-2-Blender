%rwf=methane.rwf
%nosave
%mem=64GB
%nprocshared=20
%chk=methane.chk
# opt 6-31+g(d) geom=connectivity m062x

Title Card Required

0 1
C      0.00000    0.00000    0.00000
H      0.00000    0.00000    1.08900
H      1.02672    0.00000   -0.36300
H     -0.51336   -0.88916   -0.36300
H     -0.51336    0.88916   -0.36300

 1 2 1.0 3 1.0 4 1.0 5 1.0
 2
 3
 4
 5

