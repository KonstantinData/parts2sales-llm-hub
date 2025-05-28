import pytest
from pathlib import Path


@pytest.fixture
def eval_dir():
    return Path(__file__).resolve().parent.parent / "evals"
