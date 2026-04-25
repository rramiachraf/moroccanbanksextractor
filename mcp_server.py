from mcp.server.fastmcp import FastMCP

import attijari

mcp = FastMCP("extract_bank_statement")


@mcp.tool()
async def extract_bank_statement(file_path: str) -> str:
    """Extract bank statement data from PDF into a readable Markdown
    Args:
        - Takes only the full path of the Bank statement PDF
    """
    data = attijari.parse_statement(file_path)
    response = rf"""List of transactions between {data["start_date"]} and {data["end_date"]}, the initial balance initially was {data["initial_balance"]}, and by the end of the period it was {data["balance"]}
    """
    for i, t in enumerate(data["transactions"]):
        response += rf"""## Transaction {i + 1}
    amount: {t["amount"]}
    label: {t["label"]}
    transaction_date: {t["transaction_date"]}
    value_date: {t["value_date"]}
    is_deposit: {t["is_deposit"]}

    """

    return response
