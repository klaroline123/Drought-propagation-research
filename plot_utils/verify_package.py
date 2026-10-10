"""Check the distributed SHA-256 inventory; does not contact external services."""
from pathlib import Path
import hashlib

ROOT = Path(__file__).resolve().parents[1]

if __name__ == "__main__":
    problems = []
    entries = (ROOT / "manifests/CHECKSUMS_SHA256.txt").read_text(encoding="utf-8").splitlines()
    for line in entries:
        expected, name = line.split("  ", 1)
        path = ROOT / name
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            problems.append(name)
    if problems:
        raise SystemExit("Missing or changed files: " + ", ".join(problems))
    print(f"Verified {len(entries)} files. Checksums do not establish publication permission.")
