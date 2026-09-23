import re
from datetime import UTC, date, datetime

import pdfplumber


def parse_statement(file_path: str):
    transactions = []
    initial_balance = 0
    balance = 0
    start_date = datetime.now(UTC)
    end_date = datetime.now(UTC)

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            if page.page_number == 1:
                [start_date_str, initial_balance_str] = re.findall(
                    r"SOLDE\sDEPART\sAU\s:\s(\d{2}\/\d{2}\/\d{4})\s(.*)",
                    page.crop(bbox=(10, 292, 580, 303)).extract_text(),
                )[0]
                initial_balance = float(initial_balance_str.replace(",", "."))

                [sd_day, sd_month, sd_year] = start_date_str.split("/")
                start_date = date(int(sd_year), int(sd_month), int(sd_day))

            if len(pdf.pages) == page.page_number:
                [end_date_str, balance_str] = re.findall(
                    r"NOUVEAU\sSOLDE\sAU\s(\d{2}\/\d{2}\/\d{4})\s(.*)",
                    page.crop(bbox=(70, 688, 580, 700)).extract_text(),
                )[0]
                balance = float(balance_str.replace(",", "."))

                [ed_day, ed_month, ed_year] = end_date_str.split("/")
                end_date = date(int(ed_year), int(ed_month), int(ed_day))

            table = page.crop(bbox=(10, 303, 580, 672)).extract_table(
                table_settings={
                    "horizontal_strategy": "text",
                    "intersection_tolerance": 100,
                    "min_words_horizontal": 4,
                }
            )

            if table:
                for col in table:
                    if col[1]:
                        transaction_date = col[0]
                        label = col[2]
                        value_date = col[1]
                        amount = col[3] or col[4]

                        if amount and transaction_date and value_date:
                            [v_day, v_month] = value_date.split("/")
                            [t_day, t_month] = transaction_date.split("/")

                            v_date = date(end_date.year, int(v_month), int(v_day))
                            t_date = date(end_date.year, int(t_month), int(t_day))

                            transactions.append(
                                {
                                    "transaction_date": t_date,
                                    "label": label,
                                    "value_date": v_date,
                                    "is_deposit": col[3] == "",
                                    "amount": float(amount.replace(",", ".")),
                                }
                            )

        return {
            "start_date": start_date,
            "end_date": end_date,
            "initial_balance": initial_balance,
            "balance": balance,
            "transactions": transactions,
        }
