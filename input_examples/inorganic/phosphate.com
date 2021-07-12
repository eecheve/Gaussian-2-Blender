%rwf=phosphate.rwf
%nosave
%mem=64GB
%nprocshared=20
%chk=phosphate.chk
# opt 6-31+g(d) geom=connectivity m062x

Title Card Required

-3 1
 P                  0.00000000    0.00000000    0.00000000
 O                  0.92033400    0.92033400    0.92033400
 O                 -0.92033400   -0.92033400    0.92033400
 O                 -0.92033400    0.92033400   -0.92033400
 O                  0.92033400   -0.92033400   -0.92033400

 1 2 1.5 3 1.5 4 1.5 5 1.5
 2
 3
 4
 5

