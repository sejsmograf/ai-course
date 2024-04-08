import gzip
import shutil
from csv import DictReader
import logging
from pathlib import Path
from .serialize import deserialize, serialize


PARENT_DIR_PATH: Path = Path(__file__).resolve().parent.parent

CSV_PATH: Path = PARENT_DIR_PATH / "data/connection_graph.csv"
SERIALIZED_CSV_PATH: Path = PARENT_DIR_PATH / "data/serialized_connection_graph.pickle"


def read_csv_to_dict(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        gzip_path = path.with_suffix(".csv.gz")
        print(gzip_path)
        if gzip_path.exists():
            logging.warning(f"CSV file '{path}' not found, uncompressing {gzip_path}")

            try:
                with gzip.open(gzip_path, "rb") as f_in:
                    with open(path, "wb") as f_out:
                        shutil.copyfileobj(f_in, f_out)

                    logging.info(f"Uncompressing gzip file to {path}")

            except Exception as e:
                logging.error(f"Error uncompressing: {e}")
                exit(1)
        else:
            logging.warning(
                f"File {path} not found and no correspoding compressed files"
            )
            exit(1)

    try:
        with open(path) as file:
            reader: DictReader = DictReader(file)
            data: list[dict[str, str]] = []

            for row in reader:
                data.append(row)

            return data

    except Exception as e:
        logging.error(e)
        exit(1)


def get_data(
    src_path: Path = CSV_PATH, serialized_path: Path = SERIALIZED_CSV_PATH
) -> list[dict[str, str]]:
    if serialized_path.exists():
        return deserialize(serialized_path)

    data = read_csv_to_dict(src_path)
    serialize(data, serialized_path)

    return data
