"""Run every code cell in a fresh Python process per notebook."""
from pathlib import Path
import json
import os
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

def execute(path):
    os.chdir(ROOT)
    namespace = {"__name__": "__main__"}
    notebook = json.loads(path.read_text(encoding="utf-8"))
    for index, cell in enumerate(notebook["cells"]):
        if cell["cell_type"] == "code":
            exec(compile("".join(cell["source"]), f"{path.name}:cell{index}", "exec"), namespace)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--worker":
        execute(Path(sys.argv[2]))
    else:
        paths = [ROOT / arg for arg in sys.argv[1:]] if sys.argv[1:] else sorted(
            list((ROOT / "main_figures").glob("*.ipynb"))
            + list((ROOT / "supplementary_figures").glob("*.ipynb"))
        )
        results = []
        for path in paths:
            result = subprocess.run([sys.executable, str(Path(__file__).resolve()), "--worker", str(path)])
            results.append({"notebook": path.relative_to(ROOT).as_posix(), "exit_code": result.returncode})
        (ROOT / "outputs").mkdir(exist_ok=True)
        (ROOT / "outputs" / "execution_status.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
        sys.exit(int(any(row["exit_code"] != 0 for row in results)))
