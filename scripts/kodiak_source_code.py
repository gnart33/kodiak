from berascan_api import BeraScanAPI
from contract_writer import write_contract
import json
import os

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def fetch_contracts():
    bera_scan = BeraScanAPI()
    with open("data/kodiak_contracts.json", "r") as f:
        contracts = json.load(f)["contracts"]

    for contract_name, contract_address in contracts.items():
        if os.path.exists(
            f"data/contracts_json/{contract_name}_{contract_address}.json"
        ):
            logger.info(
                f"file {contract_name}_{contract_address}.json already exists, skipping"
            )
            continue
        bera_scan.save_contract_source(
            contract_address,
            f"data/contracts_json/{contract_name}_{contract_address}.json",
        )
        logger.info(f"Saved {contract_name}_{contract_address}.json")


def write_contracts():
    # for file in os.listdir("data/contracts_json"):
    #     if file.endswith(".json"):
    #         logger.info(f"writing {file}")
    #         write_contract(f"data/contracts_json/{file}")

    f = "UniswapV3Factory_0xD84CBf0B02636E7f53dB9E5e45A616E05d710990"
    contract_json = f"data/contracts_json/{f}.json"

    write_contract(contract_json)


if __name__ == "__main__":
    # fetch_contracts()
    write_contracts()
