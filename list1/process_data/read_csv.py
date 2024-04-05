from csv import DictReader
from pathlib import Path
from .serialize import deserialize, serialize


PARENT_DIR_PATH: Path = Path(__file__).resolve().parent.parent

CSV_PATH: Path = PARENT_DIR_PATH / "data/connection_graph.csv"
SERIALIZED_CSV_PATH: Path = PARENT_DIR_PATH / "data/serilized_connection_graph.pickle"


def read_csv_to_dict(path: Path) -> list[dict[str, str]]:
    with open(path) as file:
        reader: DictReader = DictReader(file)

        data: list[dict[str, str]] = []

        for row in reader:
            data.append(row)

        return data


def get_data(
    src_path: Path = CSV_PATH, serialized_path: Path = SERIALIZED_CSV_PATH
) -> list[dict[str, str]]:
    if serialized_path.exists():
        return deserialize(serialized_path)

    data = read_csv_to_dict(src_path)
    serialize(data, serialized_path)

    return data
