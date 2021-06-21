import sys
import math

def extended_euclid(a, b):
    q = [0, 0]
    r = [a, b]
    s = [1, 0]
    t = [0, 1]
    i = 2
    while(r[-1] != 0):
        q.append(r[i-2]//r[i-1])
        r.append(r[i-2] - q[i]*r[i-1])
        s.append(s[i-2] - q[i]*s[i-1])
        t.append(t[i-2] - q[i]*t[i-1])
        i += 1
    #print(q, r, s, t)
    return (r[-2], s[-2], t[-2])


n, a, b, k, m = [int(i) for i in input().split()]
d = abs(m - k)
gcd_bezous = extended_euclid(a, b)

gcd = gcd_bezous[0]
bezous_x = gcd_bezous[1]
bezous_y = gcd_bezous[2]

u = a//gcd
v = b//gcd

for k in range(-10, 10):
    print( ((d//gcd)*(bezous_x+k*v), (d//gcd)*(bezous_y-k*u)) )

if (d%gcd) != 0:
    print("IMPOSSIBLE")
else:
    print("POSSIBLE")
