import pandas as pd


def get_amount(amount):
    ret_val = amount.strip()
    ret_val = ret_val.replace(' ', '')
    ret_val = ret_val.replace("\\n", "")
    ret_val = ret_val.replace(',', '.')

    return float(ret_val)


def get_tier_from_rules_and_memo(rules, str_memo):
    list_tier = []
    list_category = []

    for index, row in rules.iterrows():

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
        print(" error ", str_memo, list_tier, list_category)
        ret_val = list(['KO', 'KO'])

    return ret_val


def get_tiers_from_rules_and_memo_series(rules, memo_series):
    ret_val = pd.Series(memo_series)

    ret_val = ret_val.transform(lambda x: get_tier_from_rules_and_memo(rules, x)[0]), \
              ret_val.transform(lambda x: get_tier_from_rules_and_memo(rules, x)[1])

    return ret_val


def get_tiers_and_category_from_rules_and_memo_series(rules_csv, memo_series):
    rules_tier_csv = pd.read_csv(
        rules_csv,
        encoding='latin-1',
        sep=";"
    )

    return get_tiers_from_rules_and_memo_series(rules_tier_csv, memo_series)
