import pandas as pd
import releve.releve as releve
import tools.yaml_config as yc

directory_path = yc.get_path()


def df_extract_ing_releve(file_name, rules_file_name, init_solde):

    ing_csv = pd.read_csv(
        file_name,
        encoding='latin-1',
        #    error_bad_lines=False,
        sep=";"
    )

    #print(ing_csv.shape)
    #print(ing_csv)

    ret_val = ing_csv.copy()

    ret_val['date'] = pd.to_datetime(ret_val['date'], format='%d/%m/%Y')
    ret_val = ret_val.sort_values(by='date')
    ret_val['amount'] = ret_val['amount'].apply(lambda x: releve.get_amount(x))

    ret_val['category'], ret_val['tier'] = releve.get_tiers_and_category_from_rules_and_memo_series(
        rules_file_name,
        ret_val['memo']
    )

    ret_val['solde'] = ret_val['amount'].cumsum()

    print(ret_val.shape)
    print(ret_val)

    return ret_val