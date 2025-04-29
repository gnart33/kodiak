import json
import os
import logging
import filecmp
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def write_contract(contracts_json_path: str):
    """
    Write a contract to a file.
    """
    if not os.path.exists(contracts_json_path):
        raise FileNotFoundError(f"File {contracts_json_path} not found")

    with open(contracts_json_path, "r") as f:
        data = json.load(f)

    # Check if the data has the expected structure
    if not isinstance(data, dict):
        try:
            contract_name = Path(contracts_json_path).stem.split("_")[0]
            if os.path.exists(f"src/{contract_name}.sol"):
                logger.info(f"contract {contract_name} already exists, skipping")
                return
            else:
                contract_path = f"src/{contract_name}.sol"
                os.makedirs(os.path.dirname(contract_path), exist_ok=True)
                with open(contract_path, "w") as f:
                    f.write(data)
        except Exception as e:
            logger.error(f"Error writing contract {contract_name}: {e}")
            raise e

    # if "sources" not in data:
    #     raise ValueError("JSON data does not contain 'sources' key")

    else:
        contracts = data["sources"]

        for contract_path, contract_code in contracts.items():
            os.makedirs(os.path.dirname(contract_path), exist_ok=True)

            # Create a temporary file with the new content
            if os.path.exists(contract_path):
                logger.info(f"file {contract_path} already exists, skipping")
                continue

            with open(contract_path, "w") as f:
                f.write(contract_code["content"])

            logger.info(f"wrote contract to {contract_path}")


if __name__ == "__main__":
    write_contract(
        "data/contracts_json/0xD84CBf0B02636E7f53dB9E5e45A616E05d710990.json"
    )
