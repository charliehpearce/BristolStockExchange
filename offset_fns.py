### Offset Functions For BSE
import math 

def sin_schedule_offsetfn(t):
    pi2 = math.pi * 2
    c = math.pi * 3000
    wavelength = t / c
    gradient = 10 * t / (c / pi2)
    amplitude = 7.5 * t / (c / pi2)
    offset = gradient + amplitude * math.sin(wavelength * t)
    return int(round(offset, 0))

for i in range(1200):
    print(sin_schedule_offsetfn(i))