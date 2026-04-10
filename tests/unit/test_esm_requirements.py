"""Regression tests for the optional ESM requirements file."""

from pathlib import Path


def test_esm_requirements_skip_optional_stack_on_python_313():
    requirements_path = (
        Path(__file__).parent.parent.parent
        / "src"
        / "tooluniverse"
        / "remote"
        / "esm"
        / "requirements.txt"
    )
    lines = [
        line.strip()
        for line in requirements_path.read_text().splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]

    assert 'esm>=2.0.0; python_version < "3.13"' in lines
    assert 'torch>=2.0.0; python_version < "3.13"' in lines
