import json
import os
import sys
from pathlib import Path

try:
    data = json.loads(sys.stdin.read())
    transactions = data["transactions"]
    output_file = Path(os.getcwd(), f"wf_{data['start_date']}.csv")

    with open(output_file, "w") as f:
        if len(transactions) > 0:
            header = (
                "date,symbol,quantity,activityType,unitPrice,currency,amount,comment"
            )
            _ = f.write(header + "\n")

    with open(output_file, "a") as f:
        for t in transactions:
            f.writelines(
                f'{t["transaction_date"]},,1,{"TRANSFER_IN" if t["is_deposit"] else "TRANSFER_OUT"},0,MAD,{t["amount"]},"{t["label"]}"\n'
            )

except ValueError:
    print("Invalid input")
