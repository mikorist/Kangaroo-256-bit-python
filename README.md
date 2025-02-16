# Kangaroo Algorithm for Elliptic Curve Discrete Logarithm Problem (ECDLP)

This repository contains a Python implementation of the **Kangaroo Algorithm** (also known as the **Pollard's Kangaroo Algorithm**) for solving the **Elliptic Curve Discrete Logarithm Problem (ECDLP)**. The algorithm is designed to find the private key corresponding to a given public key on the **secp256k1 elliptic curve**, which is the curve used in Bitcoin and other cryptocurrencies.

This implementation is **for educational, testing, and experimental purposes only**. It is not optimized for solving real-world cryptographic challenges and will not solve anything above **puzzle 66** due to computational limitations.

This version is based on: http://fe57.org/forum/thread.php?board=4&thema=1 

---

## Table of Contents
1. [Introduction](#introduction)
2. [How It Works](#how-it-works)
3. [Usage](#usage)
4. [Limitations](#limitations)
5. [Disclaimer](#disclaimer)
6. [License](#license)

---

## Introduction

The **Kangaroo Algorithm** is a probabilistic algorithm used to solve the **Discrete Logarithm Problem (DLP)** on elliptic curves. Given a public key `Q = k * G`, where `G` is the generator point of the curve and `k` is the private key, the algorithm aims to find `k` by simulating the movements of two "kangaroos" (tame and wild) on the elliptic curve.

This implementation focuses on the **secp256k1 curve** and is designed to solve small-scale puzzles (up to **puzzle 66**) for learning and experimentation purposes.

---

## How It Works

### Key Concepts
1. **Elliptic Curve Arithmetic**:
   - The implementation uses elliptic curve point addition and scalar multiplication to perform operations on the secp256k1 curve.
   - The curve parameters (modulo, order, generator point) are defined according to the secp256k1 standard.

2. **Kangaroo Algorithm**:
   - The algorithm uses two "herds" of kangaroos: the **tame kangaroos** and the **wild kangaroos**.
   - Tame kangaroos start from a known point within the range, while wild kangaroos start from the public key.
   - Both herds "hop" around the curve using a pseudo-random function (based on powers of two).
   - When a kangaroo lands on a **distinguished point (DP)**, it is stored in a lookup table.
   - If a tame kangaroo and a wild kangaroo land on the same distinguished point, the private key can be computed.

3. **Distinguished Points (DPs)**:
   - Distinguished points are points on the curve that satisfy a specific condition (e.g., their x-coordinate modulo a rarity value equals zero).
   - DPs are used to reduce the number of points that need to be stored and compared.

4. **Inverse Kangaroo**:
   - An additional optimization is implemented to handle the inverse of the public key, which can speed up the search in certain cases.

---

## Usage

### Prerequisites
- Python 3.x
- The `gmpy2` library for efficient large integer arithmetic.

Install the required library using:
```
pip3 install gmpy2
```

# Running the Algorithm
Clone the repository:
```
git clone https://github.com/mikorist/Kangaroo-256-bit-python.git
cd Kangaroo-256-bit-python
```

#  Modify the parameters in the script:
<ul>
  <li>puzzle: The size of the puzzle (e.g., 40 for a 40-bit private key).</li>

  <li>compressed_public_key: The public key to solve (in compressed format).</li>

  <li>kangaroo_power: Controls the number of kangaroos in each herd (2^kangaroo_power).</li>
</ul>

# Run the script:
```
python3 kangaroo.py
```

# The script will output:

<ul>
  <li>The number of hops performed.</li>

  <li>The private key if found.</li>

  <li>The total time taken.</li>
</ul>

```
[+] Kangaroo: Sun Feb 16 13:16:20 2025
[+] Puzzle: 40
[+] Lower range limit: 549755813888
[+] Upper range limit: 1099511627775
[+] DP: 2^10 (1024)
[+] Expected Hops: 2^21.00 (2097152)
[+] Hops: 2^19.89 <-> 323987 h/s  
[+] PUZZLE SOLVED 
[+] Private key (dec): 1003651412950 
[+] Total Hops: 973872
[+] Total time: 3.1 seconds
```
---

## Limitations
Puzzle Size:
<ul>
  <li>This implementation is designed for small puzzles (up to puzzle 66). Solving larger puzzles requires significant computational resources and is not feasible with this code.</li>
</ul>
Performance:
<ul>
  <li>The algorithm is not optimized for speed. It is intended for educational purposes and may take a long time to solve even small puzzles.</li>
</ul>
Real-World Use:
<ul>
  <li>This code is not suitable for real-world cryptographic challenges. It is meant for learning and experimentation only.</li>
</ul>

---

## Disclaimer
This software is provided as-is and is intended only for educational, testing, and experimental purposes. It is not designed to solve real-world cryptographic problems or to be used in any production environment. The author is not responsible for any misuse of this software.

---

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

# Acknowledgments
The algorithm is based on the original work by Pollard and subsequent improvements by the cryptographic community.

The elliptic curve arithmetic is implemented using the secp256k1 parameters.

Happy learning and experimenting! 🦘