%rwf=hexacyanoferrate-ii.rwf
%nosave
%mem=64GB
%nprocshared=20
%chk=hexacyanoferrate-ii.chk
# opt 6-31+g(d) geom=connectivity m062x

Title Card Required

-2 1
 Fe                 0.00000000    0.00000000    0.00000000
 C                  0.00000000    0.00000000    1.96862100
 N                  0.00000000    0.00000000    3.13221500
 C                  0.00000000    1.96863600    0.00000000
 N                  0.00000000    3.13221000    0.00000000
 C                 -1.96869900    0.00000000    0.00000000
 N                 -3.13234100    0.00000000    0.00000000
 C                  0.00000000    0.00000000   -1.96862100
 N                  0.00000000    0.00000000   -3.13221500
 C                  1.96869900    0.00000000    0.00000000
 N                  3.13234100    0.00000000    0.00000000
 C                  0.00000000   -1.96863600    0.00000000
 N                  0.00000000   -3.13221000    0.00000000

 1 2 1.0 4 1.0 6 1.0 8 1.0 10 1.0 12 1.0
 2 3 3.0
 3
 4 5 3.0
 5
 6 7 3.0
 7
 8 9 3.0
 9
 10 11 3.0
 11
 12 13 3.0
 13

