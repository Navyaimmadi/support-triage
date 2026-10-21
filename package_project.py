"""Package source and reviewed evidence, excluding credentials and runtime state."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

root = Path(__file__).resolve().parent
target = root.parent / "multi-agent-support-triage.zip"
excluded = {".venv", "__pycache__", ".pytest_cache", "runtime", ".git"}
with ZipFile(target, "w", ZIP_DEFLATED) as archive:
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        is_private_env = path.name.startswith(".env") and path.name != ".env.example"
        if path.is_file() and not (set(relative.parts) & excluded) and not is_private_env and ".db" not in path.name and path.name != ".DS_Store":
            archive.write(path, Path(root.name) / relative)
print(target)
