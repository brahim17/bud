import re
from datetime import datetime

import pandas as pd

import tools.yaml_config as yc

START_DATE_PATTERN = "^[0-9][0-9]\.[0-9][0-9] "
DATE_PATTERN = "[0-9][0-9]\.[0-9][0-9]"
directory_path = yc.get_path()


def get_amount(amount):
    ret_val = amount.strip()
    ret_val = ret_val.replace(' ', '')
    ret_val = ret_val.replace("\\n", "")
    ret_val = ret_val.replace(',', '.')

    return float(ret_val)


def get_date(p_date, year):
    ret_val = p_date.strip()
    ret_val += "." + year

    return datetime.strptime(ret_val, '%d.%m.%y')


def get_tier_from_rules_and_memo(rules_tier_csv, str_memo):

    list_tier = []
    list_category = []

    for index, row in rules_tier_csv.iterrows():

        category = str(row['CATEGORY'])
        tier = str(row['TIER'])
        tier_pattern = str(row['PATTERN'])

        if tier_pattern.lower() in str_memo.lower():
            list_tier.append(tier)
            list_category.append(category)

    ret_val = None

    list_tier = set(list_tier)
    list_category = set(list_category)

    if len(list_tier) == 1:
        ret_val = list([list_category.pop(), list_tier.pop()])
    else:
        print( " error ", str_memo, list_tier, list_category)
        ret_val = list(['KO', 'KO'])

    return ret_val


def get_tiers_from_rules_and_memo_series(rules_csv, memo_series):
    rules_tier_csv = pd.read_csv(
        rules_csv,
        encoding='latin-1',
        sep=";"
    )

    ret_val = pd.Series(memo_series)

    ret_val = ret_val.transform(lambda x: get_tier_from_rules_and_memo(rules_tier_csv, x)[0]), ret_val.transform(lambda x: get_tier_from_rules_and_memo(rules_tier_csv, x)[1])

    return ret_val


def extract_bnp_releve(year, init_solde):
    f = open(directory_path + "bnp-raw/bnp-20" + year + ".txt", "r")

    transactions = []
    memo = None
    solde = init_solde

    for line in f:

        newline = re.search(START_DATE_PATTERN, line)

        # new line
        if newline is not None and newline.start() == 0:

            tr_dates = re.findall(DATE_PATTERN, line)

            date1 = tr_dates[0].strip()
            date2 = tr_dates[1].strip()
            amount = ""

            if len(tr_dates) == 2:
                tr_memo_amount = re.split(DATE_PATTERN, line)
                memo = tr_memo_amount[1]
                amount = tr_memo_amount[2]
            else:
                print("Warning")

            float_amount = get_amount(amount)
            if solde is None:
                solde = float_amount
            else:
                solde += float_amount

            transactions.append(
                [get_date(date1, year), memo.strip(), get_date(date2, year), get_amount(amount), round(solde, 2)]
            )

        else:
            if memo is not None:
                memo += " " + line.strip()
                transactions[-1][1] = memo

    f.close()

    df_bnp = pd.DataFrame(transactions, columns=['date', 'memo', 'date2', 'amount', 'solde'])

    df_bnp['category'], df_bnp['tier'] = get_tiers_from_rules_and_memo_series(
        #directory_path + "tier-rules-bnp.csv",
        directory_path + "bnp-rules.csv",
        df_bnp['memo']
    )

    return df_bnp


def df_extract_bnp_releve(init_solde):
    ret_val = pd.DataFrame(
        columns=['date', 'memo', 'date2', 'amount', 'solde']
    )

    for y in ["16", "17", "18", "19", "20", "21"]:
        df = extract_bnp_releve(y, init_solde)
        init_solde = df['solde'].iloc[[-1]].values[0]

        ret_val = pd.concat([ret_val, df])

    return ret_val
