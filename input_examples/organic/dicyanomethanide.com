%rwf=dicyanomethanide.rwf
%nosave
%mem=64GB
%nprocshared=20
%chk=dicyanomethanide.chk
# opt 6-31+g(d) geom=connectivity m062x

Title Card Required

-1 1
 C                  0.00000000    0.00000000    0.72570800
 H                  0.00000000    0.00000000    1.80823200
 C                  0.00000000    1.22526500    0.05194200
 N                  0.00000000    2.26923000   -0.48469900
 C                  0.00000000   -1.22526500    0.05194200
 N                  0.00000000   -2.26923000   -0.48469900

 1 2 1.0 3 1.5 5 1.5
 2
 3 4 3.0
 4
 5 6 3.0
 6

