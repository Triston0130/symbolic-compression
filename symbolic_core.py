# symbolic_core.py

import numpy as np

# === Collapse-Based Compression ===

class SymbolicCompressor:
    def __init__(self, x0=None, delta0=None, kappa=None, N=None):
        self.x0 = x0
        self.delta0 = delta0
        self.kappa = kappa
        self.N = N

    def compress(self, sequence):
        if len(sequence) < 3:
            raise ValueError("Sequence too short to compress.")
        intervals = np.diff(sequence)
        self.delta0 = intervals[0]
        self.kappa = np.mean(intervals[1:] / intervals[:-1])
        self.x0 = sequence[0]
        self.N = len(sequence)
        return {'x0': self.x0, 'delta0': self.delta0, 'kappa': self.kappa, 'N': self.N}

    def decompress(self):
        if None in (self.x0, self.delta0, self.kappa, self.N):
            raise ValueError("Missing compression parameters.")
        values = [self.x0]
        for i in range(1, self.N):
            values.append(values[-1] + self.delta0 * (self.kappa ** (i - 1)))
        return values


class MultiZoneSymbolicCompressor:
    def __init__(self, segment_length=20):
        self.segment_length = segment_length
        self.segments = []

    def compress(self, sequence):
        self.segments = []
        for i in range(0, len(sequence), self.segment_length):
            seg = sequence[i:i + self.segment_length]
            if len(seg) < 3:
                continue
            sc = SymbolicCompressor()
            try:
                rule = sc.compress(seg)
                rule['zone_start'] = i
                rule['zone_end'] = i + len(seg) - 1
                self.segments.append(rule)
            except Exception:
                continue
        return self.segments

    def decompress(self):
        full = []
        for rule in self.segments:
            sc = SymbolicCompressor(
                x0=rule['x0'],
                delta0=rule['delta0'],
                kappa=rule['kappa'],
                N=rule['N']
            )
            full.extend(sc.decompress())
        return full


# === Recursive Function Compression ===

class RecursiveFunctionCompressor:
    def __init__(self, initial_values, recurrence_function, N):
        self.initial_values = initial_values
        self.recurrence_function = recurrence_function
        self.N = N

    def decompress(self):
        sequence = self.initial_values[:]
        for n in range(len(self.initial_values), self.N):
            next_val = self.recurrence_function(sequence, n)
            sequence.append(next_val)
        return sequence


# === Recurrence Rule Library ===

def fibonacci_rule(seq, n):
    return seq[n - 1] + seq[n - 2]

def tribonacci_rule(seq, n):
    return seq[n - 1] + seq[n - 2] + seq[n - 3]

def catalan_rule(seq, n):
    return int(seq[n - 1] * 2 * (2 * n - 1) / (n + 1))

def factorial_rule(seq, n):
    return n * seq[n - 1] if n > 1 else 1

def fibonacci_golden_ratio_rule(seq, n):
    phi = (1 + 5 ** 0.5) / 2
    return int(round(phi ** n / 5 ** 0.5))

def lucas_rule(seq, n):
    return seq[n - 1] + seq[n - 2]

def pell_rule(seq, n):
    return 2 * seq[n - 1] + seq[n - 2]

def is_squarefree(n):
    for i in range(2, int(n ** 0.5) + 1):
        if n % (i * i) == 0:
            return False
    return True

def squarefree_rule(seq, n):
    current = seq[-1] + 1
    while not is_squarefree(current):
        current += 1
    return current

def prime_rule(seq, n):
    current = seq[-1] + 1
    while not all(current % i != 0 for i in range(2, int(current ** 0.5) + 1)):
        current += 1
    return current

def harmonic_rule(seq, n):
    return seq[-1] + 1 / n

def triangular_rule(seq, n):
    return seq[-1] + n

def bell_number_rule(seq, n):
    return sum(seq[i] * seq[n - i - 1] for i in range(n))

def power_rule(seq, n, k=2):
    return n ** k

def custom_fibonacci_rule(seq, n, m=3):
    return sum(seq[n - i - 1] for i in range(m))

def sum_of_divisors_rule(seq, n):
    divisors_sum = sum(i for i in range(1, n+1) if n % i == 0)
    return divisors_sum

def square_numbers_rule(seq, n):
    return n ** 2

def prime_factorization_rule(seq, n):
    factors = []
    i = 2
    while n > 1:
        while n % i == 0:
            factors.append(i)
            n //= i
        i += 1
    return factors

def look_and_say_rule(seq, n):
    prev_term = str(seq[n - 1])
    result = []
    count = 1
    for i in range(1, len(prev_term)):
        if prev_term[i] == prev_term[i - 1]:
            count += 1
        else:
            result.append(f"{count}{prev_term[i - 1]}")
            count = 1
    result.append(f"{count}{prev_term[-1]}")
    return int(''.join(result))



recurrence_rules = {
    "fibonacci": (fibonacci_rule, [0, 1]),
    "tribonacci": (tribonacci_rule, [0, 1, 1]),
    "catalan": (catalan_rule, [1]),
    "factorial": (factorial_rule, [1]),
    "fibonacci_approx": (fibonacci_golden_ratio_rule, [0, 1]),
    "lucas": (lucas_rule, [2, 1]),
    "pell": (pell_rule, [0, 1]),
    "squarefree": (squarefree_rule, [1]),
    "prime": (prime_rule, [2]),
    "harmonic": (harmonic_rule, [1]),
    "triangular": (triangular_rule, [1]),
    "bell": (bell_number_rule, [1]),
    "power": (power_rule, [1]),
    "custom_fibonacci": (custom_fibonacci_rule, [1, 1, 2]),
    "sum_of_divisors": (sum_of_divisors_rule, [1]),
    "squares": (square_numbers_rule, [1]),
    "prime_factors": (prime_factorization_rule, [2]),
    "look_and_say": (look_and_say_rule, [1]),
}
