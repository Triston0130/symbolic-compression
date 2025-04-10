# Symbolic Compression Engine

**A universal compression system for symbolic, recursive, and irreducible structures.**

This open-source engine encodes symbolic data (like primes, Fibonacci, or custom sequences) by extracting recurrence rules and structural curvature—compressing information not by repetition, but by regenerable symbolic logic.

---

## Features

- **Collapse-Based Multi-Zone Compression**  
  Segment symbolic data into curvature-aware zones and extract recurrence rules per zone.

- **Recursive Function Encoding**  
  Compress sequences using rule-based recurrence (e.g. Fibonacci, Tribonacci, Catalan, etc.).

- **Predictive Decompression**  
  Regenerate full sequences from stored `.sym` rule files—symbolic memory without storing data.

- **Structured `.sym` Format**  
  Stores symbolic rules, curvature parameters, metadata, and regeneration length.

- **Command-Line Interface (CLI)**  
  Compress, decompress, collapse, or predict using simple terminal commands.

---

## Quick Start

### Clone the repo:

```bash
git clone https://github.com/YOUR_USERNAME/symbolic-compression.git
cd symbolic-compression
```

### Compress a symbolic sequence using built-in rules:

```bash
python symbolic_cli.py compress fibonacci --length 20 --output fib.sym
```

### Collapse a symbolic sequence (e.g. primes) into multi-zone form:

```bash
python symbolic_cli.py collapse --output primes.sym --segment-length 5
```

### Predict from a `.sym` file:

```bash
python symbolic_cli.py predict primes.sym --output regenerated.txt
```

## Example `.sym` File (Human-Readable)

```json
{
  "format": "symbolic-collapse-v2",
  "type": "multi-zone",
  "rules": [
    {
      "x0": 2,
      "delta0": 1,
      "kappa": 1.5,
      "N": 5
    }
  ],
  "metadata": {
    "domain": "collapse",
    "created_by": "Triston Miller",
    "timestamp": "2025-04-10T..."
  }
}
```

## Applications

- Compression of irreducible sequences (primes, squarefree, symbolic logic)
- AI memory modeling and regeneration
- Mathematical structure archiving
- Generative storage systems
- Time series symbolic abstraction
- Post-ZIP compression paradigms

## Author

**Triston Miller**  
Creator of Symbolic Field Theory and the Symbolic Compression Engine.  
Filed provisional patent #63/786,260 — April 2025.

## License

MIT License  
(You may fork, extend, and use non-commercially. Contact for licensing.)
