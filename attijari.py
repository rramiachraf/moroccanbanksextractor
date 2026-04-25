import re
from datetime import date

import pdfplumber


def parse_statement(file_path: str):
    transactions = []
    initial_balance = 0
    balance = 0
    start_date = date.today()
    end_date = date.today()

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            if page.page_number == 1:
                [start_date_str, initial_balance_str] = re.findall(
                    r"SOLDE\sDEPART\sAU\s(\d{2}\s\d{2}\s\d{4})\s(.*)\sCREDITEUR",
                    page.crop(bbox=(140, 310, 620, 347)).extract_text(),
                )[0]
                initial_balance = float(
                    initial_balance_str.replace(",", ".").replace(" ", "")
                )

                [sd_day, sd_month, sd_year] = start_date_str.split(" ")
                start_date = date(int(sd_year), int(sd_month), int(sd_day))

            if len(pdf.pages) == page.page_number:
                [end_date_str, balance_str] = re.findall(
                    r"S\s?O\s?L\s?D\s?E\sF\s?I\s?N\s?A\s?L\sA\s?U\s(\d\s?\d\s\d\s?\d\s\d\s?\d\s?\d\s?\d)\s(.*)\sC\s?R\s?E\s?D\s?I\s?T\s?E\s?U\s?R",
                    page.crop(bbox=(140, 703, 625, 738)).extract_text(),
                )[0]
                balance = float(balance_str.replace(",", ".").replace(" ", ""))

                [ed_day, ed_month, ed_year] = clean_date(end_date_str).split(" ")
                end_date = date(int(ed_year), int(ed_month), int(ed_day))

            table = page.crop(bbox=(14, 373, 601, 700)).extract_table(
                table_settings={
                    "horizontal_strategy": "text",
                    "intersection_tolerance": 100,
                    "min_words_horizontal": 4,
                }
            )

            if table:
                for col in table:
                    if col[1]:
                        transaction_date = col[2]
                        label = col[3]
                        value_date = col[4]
                        amount = col[5] or col[6]

                        if amount and transaction_date and value_date:
                            [v_day, v_month, v_year] = clean_date(value_date).split(" ")
                            [t_day, t_month] = clean_date(transaction_date).split(" ")

                            v_date = date(int(v_year), int(v_month), int(v_day))
                            t_date = date(int(v_year), int(t_month), int(t_day))

                            transactions.append(
                                {
                                    "transaction_date": t_date,
                                    "label": label,
                                    "value_date": v_date,
                                    "is_deposit": col[5] == "",
                                    "amount": float(
                                        amount.replace(",", ".").replace(" ", "")
                                    ),
                                }
                            )

        return {
            "start_date": start_date,
            "end_date": end_date,
            "initial_balance": initial_balance,
            "balance": balance,
            "transactions": transactions,
        }


def clean_date(date_str: str):
    date = ""
    for i, char in enumerate(date_str.replace(" ", "")):
        if i == 2 or i == 4:
            date += " "
        date += char
    return date
