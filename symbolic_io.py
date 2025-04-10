# symbolic_io.py
import numpy as np
import json
from datetime import datetime


def save_recursive_to_sym(rule_name, initial_values, N, rule_expr, filename, created_by="Kay", domain="symbolic"):
    print(f"Attempting to save data to {filename}...")  # Debugging line
    data = {
        "format": "symbolic-compression-v1",
        "type": "recursive",
        "sequence_name": rule_name,
        "length": N,
        "initial_values": initial_values,
        "rule": rule_expr,
        "rule_id": rule_name,
        "metadata": {
            "domain": domain,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    }
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
    print(f"File saved to {filename}")  # Debugging line


def load_recursive_from_sym(filename):
    with open(filename, "r") as f:
        data = json.load(f)
    return data["rule_id"], data["initial_values"], data["length"]

def save_collapse_to_sym(segments, filename, created_by="TM", domain="collapse"):
    print(f"Saving multi-zone .sym to {filename}...")

    # Convert all NumPy types to native Python types for JSON
    clean_segments = []
    for rule in segments:
        clean_rule = {k: int(v) if isinstance(v, (np.integer,)) else float(v) if isinstance(v, (np.floating,)) else v
                      for k, v in rule.items()}
        clean_segments.append(clean_rule)

    data = {
        "format": "symbolic-collapse-v2",
        "type": "multi-zone",
        "rules": clean_segments,
        "metadata": {
            "domain": domain,
            "created_by": created_by,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    }

    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

    print(f"Saved {len(clean_segments)} rule zones to {filename}")


def load_collapse_from_sym(filename):
    with open(filename, "r") as f:
        data = json.load(f)
    return data["segments"]

def load_collapse_from_sym(filename):
    with open(filename, "r") as f:
        data = json.load(f)
    return data["rules"]
