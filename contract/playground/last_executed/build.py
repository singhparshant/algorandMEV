# Build the sample contract in this directory using Beaker and output to ./artifacts
from pathlib import Path

import last_executed


def build() -> Path:
    """Build the beaker app, export it to disk, and return the Path to the app spec file"""
    app_spec = last_executed.last_executed.build()
    output_dir = Path(__file__).parent / "artifacts"
    print(f"Dumping {app_spec.contract.name} to {output_dir}")
    app_spec.export(output_dir)
    return output_dir / "last_executed.json"


if __name__ == "__main__":
    build()
