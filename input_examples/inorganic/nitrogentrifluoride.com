%rwf=nitrogentrifluoride.rwf
%nosave
%mem=64GB
%nprocshared=20
%chk=nitrogentrifluoride.chk
# opt 6-31+g(d) geom=connectivity m062x

Title Card Required

0 1
 N                  -0.0156    1.2958    0.0092
 F                  -0.7092    1.7578   -0.9885
 F                   1.1916    1.7781    0.0002
 F                   0.0021   -0.0041    0.0020

 1 2 1.0 3 1.0 4 1.0
 2
 3
 4

