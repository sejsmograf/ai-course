import pickle
from typing import Any
from pathlib import Path


def serialize(data: Any, path: Path):
    with open(path, "wb") as file:
        pickle.dump(data, file)


def deserialize(path: Path) -> Any:
    with open(path, "rb") as file:
        data = pickle.loads(file.read())

        return data
