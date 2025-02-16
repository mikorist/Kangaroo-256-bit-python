# based on http://fe57.org/forum/thread.php?board=4&thema=1
import time, os, sys, random
from gmpy2 import mpz, powmod, invert, jacobi
from math import log2, sqrt, log

# Clear screen and initialize
os.system("cls||clear")
t = time.ctime()
sys.stdout.write(f"\033[?25l\033[01;33m[+] Kangaroo: {t}\n")
sys.stdout.flush()

# Elliptic Curve Parameters
modulo = mpz(0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F)
order = mpz(0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141)
Gx = mpz(0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798)
Gy = mpz(0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)
PG = (Gx, Gy)

# Point Addition on Elliptic Curve
def add(P, Q):
    if P == (0, 0):
        return Q
    if Q == (0, 0):
        return P
    
    Px, Py = P
    Qx, Qy = Q

    if Px == Qx:
        if Py == Qy:
            inv_2Py = invert((Py << 1) % modulo, modulo)
            m = (3 * Px * Px * inv_2Py) % modulo
        else:
            return (0, 0)
    else:
        inv_diff_x = invert(Qx - Px, modulo)
        m = ((Qy - Py) * inv_diff_x) % modulo

    x = (m * m - Px - Qx) % modulo
    y = (m * (Px - x) - Py) % modulo
    return (x, y)

# Scalar Multiplication on Elliptic Curve
def mul(k, P=PG):
    R0, R1 = (0, 0), P
    for i in reversed(range(k.bit_length())):
        if (k >> i) & 1:
            R0, R1 = add(R0, R1), add(R1, R1)
        else:
            R1, R0 = add(R0, R1), add(R0, R0)
    return R0

# Point Subtraction
def point_subtraction(P, Q):
    Q_neg = (Q[0], (-Q[1]) % modulo)
    return add(P, Q_neg)

# Compute Y from X using curve equation
def X2Y(X, y_parity, p=modulo):
    X3_7 = (pow(X, 3, p) + 7) % p
    if jacobi(X3_7, p) != 1:
        return None
    Y = powmod(X3_7, (p + 1) >> 2, p)
    return Y if (Y & 1) == y_parity else (p - Y)

# Generate Powers of Two
def generate_powers_of_two(hop_modulo):
    return [1 << pw for pw in range(hop_modulo)]

# Handle Solution
def handle_solution(solution):
    HEX = f"{abs(solution):064x}"
    dec = int(HEX, 16)
    print(f"\n\033[32m[+] PUZZLE SOLVED \033[0m")
    print(f"\033[32m[+] Private key (dec): {dec} \033[0m")
    with open("KEYFOUNDKEYFOUND.txt", "a") as file:
        file.write(f"\n\nSOLVED {t}\nPrivate Key (decimal): {dec}\nPrivate Key (hex): {HEX}\n{'-' * 100}\n")
    return True

# Kangaroo Algorithm
def kangaroo():
    solved = False
    t = [random.randint(1 << (puzzle - 1), (1 << puzzle) - 1) for _ in range(Nt)]
    w = [random.randint(1, 1 << (puzzle - 2)) for _ in range(Nw)]
    wi = [random.randint(1, 1 << (puzzle - 2)) for _ in range(Nw)]    
    T = [mul(ti) for ti in t]
    W = [add(W0, mul(wk)) for wk in w]
    Wi = [add(W1, mul(wik)) for wik in wi]    
    tame_dps, wild_dps, wild_dps_inv = {}, {}, {}
    Hops, Hops_old = 0, 0
    t0 = time.time()
    starttime = time.time()
    while not solved:
        # Tame Herd
        for k in range(Nt):
            Hops += 1
            Tk_x = T[k][0]
            pw = Tk_x % hop_modulo
            dt = powers_of_two[pw]            
            if Tk_x % DP_rarity == 0:
                if Tk_x in wild_dps:
                    solved = handle_solution(wild_dps[Tk_x] - t[k])
                    break
                elif Tk_x in wild_dps_inv:
                    solved = handle_solution(inverse_find - (t[k] - wild_dps_inv[Tk_x]))
                    break
                tame_dps[Tk_x] = t[k]            
            t[k] += dt
            T[k] = add(P[pw], T[k])        
        if solved: break
        # Wild Herd
        for k in range(Nw):
            Hops += 1
            Wk_x = W[k][0]
            pw = Wk_x % hop_modulo
            dw = powers_of_two[pw]            
            if Wk_x % DP_rarity == 0:
                if Wk_x in tame_dps:
                    solved = handle_solution(w[k] - tame_dps[Wk_x])
                    break
                wild_dps[Wk_x] = w[k]           
            w[k] += dw
            W[k] = add(P[pw], W[k])        
        if solved: break
        # Inverse Wild Herd
        for k in range(Nw):
            Hops += 1
            Wik_x = Wi[k][0]
            pw = Wik_x % hop_modulo
            dwi = powers_of_two[pw]          
            if Wik_x % DP_rarity == 0:
                if Wik_x in tame_dps:
                    solved = handle_solution(inverse_find - (tame_dps[Wik_x] - wi[k]))
                    break
                wild_dps_inv[Wik_x] = wi[k]         
            wi[k] += dwi
            Wi[k] = add(P[pw], Wi[k])        
        if solved: break

        # Progress Update
        t1 = time.time()
        if (t1 - t0) > 3:
            hops_log = f'{log2(Hops):.2f}' if Hops > 0 else '0.00'
            sys.stdout.write(f'\r[+] Hops: 2^{hops_log} <-> {((Hops - Hops_old) / (t1 - t0)):.0f} h/s  ')
            t0 = t1
            Hops_old = Hops
    hops_list.append(Hops)        
    print(f'[+] Total Hops: {Hops}')

# Configuration
puzzle = 40
compressed_public_key = "03a2efa402fd5268400c77c20e574ba86409ededee7c4020e4b9f0edbee53de0d4"
kangaroo_power = 7
start, end = 2**(puzzle-1), (2**puzzle) - 1
DP_rarity = 1 << ((puzzle - 1) // 2 - 2) // 2 + 2
hop_modulo = round(log(2**puzzle)+5)
Nt = Nw = 2**kangaroo_power
powers_of_two = generate_powers_of_two(hop_modulo)

# Parse Public Key
if len(compressed_public_key) == 66:
    X = mpz(int(compressed_public_key[2:66], 16))
    Y = X2Y(X, int(compressed_public_key[:2]) - 2)
else:
    print("[error] Public key length invalid!")
    sys.exit(1)

W0 = (X, Y)
P = [PG]

for _ in range(hop_modulo):
    P.append(mul(2, P[-1]))

start_point = mul(start)
end_point = mul(end)
inverse_find = start + end
inverse_find_point = add(start_point, end_point)
W1 = point_subtraction(inverse_find_point, W0)

starttime = time.time()
print(f"[+] Puzzle: {puzzle}")
print(f"[+] Lower range limit: {start}")
print(f"[+] Upper range limit: {end}")
print(f"[+] DP: 2^{int(log2(DP_rarity))} ({DP_rarity:d})")
print(f"[+] Expected Hops: 2^{log2(2 * sqrt(1 << puzzle)):.2f} ({int(2 * sqrt(1 << puzzle))})")

Hops = 0
random.seed()
hops_list = []
kangaroo()
print(f"[+] Total time: {time.time() - starttime:.1f} seconds")