"""
MoroccanBanksExtractor.

Usage:
    ./main.py extract [--json | --csv] <input_file>
    ./main.py mcp [--http | --stdio | --sse]
    ./main.py -h | --help
    ./main.py --version

Arguments:
    input_file     The bank statement, must be a PDF file

Options:
    -h, --help       Print this.
    --version        Print version.
"""

import json
import os
from pathlib import Path

from docopt import docopt

import attijari
from mcp_server import mcp

if __name__ == "__main__":
    args = docopt(__doc__, version="0.1.1")

    extract_cmd = args["extract"]
    mcp_cmd = args["mcp"]

    if extract_cmd:
        is_csv = args["--csv"]
        is_json = args["--json"]

        input_file = args["<input_file>"]

        if not Path(input_file).exists():
            print("Input file not found")
            exit(1)

        data = attijari.parse_statement(file_path=input_file)

        output_file = Path(
            os.getcwd(), f"statement_{data['start_date']}.{'csv' if is_csv else 'json'}"
        )
        print("Saving to", output_file)

        if is_csv:
            with open(output_file, "w") as f:
                transactions = data["transactions"]
                if len(transactions) > 0:
                    header = ",".join(transactions[0].keys())
                    _ = f.write(header + "\n")

            with open(output_file, "a") as f:
                for t in data["transactions"]:
                    f.write(
                        f'{t["transaction_date"]},"{t["label"]}",{t["value_date"]},{t["is_deposit"]},{t["amount"]}\n'
                    )

            exit(0)

        with open(output_file, "w") as f:
            f.write(json.dumps(data, default=str, indent=4))

    if mcp_cmd:
        sse = args["--sse"]
        http = args["--http"]
        stdio = args["--stdio"]

        mcp.run(transport="stdio" if stdio else "sse" if http else "streamable-http")
