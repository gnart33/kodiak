import os
from typing import Optional, Dict, Any
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class BeraScanAPI:
    """A class to interact with BeraScan API for fetching contract information."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the BeraScan API client.

        Args:
            api_key (str, optional): BeraScan API key. If not provided, will try to get from environment variable.
        """
        self.api_key = api_key or os.getenv("BERASCAN_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key is required. Either pass it directly or set BERASCAN_API_KEY environment variable."
            )

        self.base_url = "https://api.berascan.com/api"

    def _make_request(self, module: str, action: str, address: str) -> Dict[str, Any]:
        """
        Make a request to the BeraScan API.

        Args:
            module (str): The API module to call.
            action (str): The action to perform.
            address (str): The contract address.

        Returns:
            dict: The API response data.

        Raises:
            requests.exceptions.RequestException: If the API request fails.
            ValueError: If the response indicates an error.
        """
        params = {
            "module": module,
            "action": action,
            "address": address,
            "apikey": self.api_key,
        }

        response = requests.get(self.base_url, params=params)
        response.raise_for_status()

        data = response.json()

        if data["status"] != "1":
            raise ValueError(f"API Error: {data.get('message', 'Unknown error')}")

        return data["result"]

    def get_contract_abi(self, contract_address: str) -> str:
        """
        Fetch the ABI for a verified contract.

        Args:
            contract_address (str): The address of the contract to fetch ABI for.

        Returns:
            str: The contract ABI as a JSON string.
        """
        return self._make_request("contract", "getabi", contract_address)

    def get_contract_code(self, contract_address: str) -> Dict[str, Any]:
        """
        Fetch the source code for a verified contract.

        Args:
            contract_address (str): The address of the contract to fetch source code for.

        Returns:
            Dict[str, Any]: The contract source code information including:
                - SourceCode: The actual source code
                - ABI: The contract ABI
                - ContractName: The name of the contract
                - CompilerVersion: The compiler version used
                - OptimizationUsed: Whether optimization was used
                - Runs: Number of optimization runs
                - ConstructorArguments: Constructor arguments
                - Library: Library information
                - LicenseType: The license type
                - Proxy: Whether the contract is a proxy
                - Implementation: Implementation address if proxy
                - SwarmSource: Swarm source if available
        """
        result = self._make_request("contract", "getsourcecode", contract_address)
        if isinstance(result, list) and len(result) > 0:
            return result[0]
        return result

    def save_contract_source(self, contract_address: str, output_file: str) -> None:
        """
        Fetch and save the contract source code to a file.

        Args:
            contract_address (str): The address of the contract
            output_file (str): The output file path (default: source_code.json)
        """
        source_code = self.get_contract_code(contract_address)
        if source_code["SourceCode"].startswith("{{"):  # Handle nested JSON format
            source_data = json.loads(
                source_code["SourceCode"][1:-1]
            )  # Remove outer curly braces
        else:
            source_data = source_code["SourceCode"]

        with open(output_file, "w") as f:
            json.dump(source_data, f, indent=2)


# Example usage:
if __name__ == "__main__":
    # Example contract address
    contract_address = "0xD84CBf0B02636E7f53dB9E5e45A616E05d710990"

    try:
        # Initialize the API client
        bera_scan = BeraScanAPI()

        # Fetch and save the contract source code
        bera_scan.save_contract_source(
            contract_address,
            output_file=f"data/contracts_json/{contract_address}.json",
        )
        print(f"Successfully fetched source code for contract {contract_address}")

    except Exception as e:
        print(f"Error: {e}")
