import releve.bnp_releve as releve
import releve.ing_releve as ing
import visualize.bnp_view as view
import tools.yaml_config as yc
import pandas as pd
import logging

directory_path = yc.get_path()

if __name__ == '__main__':

    logging.basicConfig(
        filename='bud_log.log',
        level=logging.INFO,
        format='%(asctime)s -- %(name)s -- %(levelname)s -- %(message)s'
    )

    logging.info("start")

    #df_bnp = releve.df_extract_bnp_releve(None)
    #df_bnp.to_csv(directory_path + "bnp-raw-3.0.csv")

    #view.plot_bar(df_bnp)
    #view.plot_pie(df_bnp)

    #df_ing = ing.df_extract_ing_releve(0)
    #df_ing.to_csv(directory_path + "ing-raw-1.5.csv")
    #view.plot_bar(df_ing)
    #view.plot_pie(df_ing,'category')

    #extraction
    file = directory_path + "ing-raw-2.0.csv"
    df_ing = ing.df_extract_ing_releve(directory_path + "ing_raw.csv", directory_path + "ing-rules.csv",  0)
    df_ing.to_csv(file, index=False)

    df_ing_raw = pd.read_csv(
        file,
        encoding='latin-1',
        #    error_bad_lines=False,
        sep=","
    )

    view.plot_pie(df_ing_raw, 'category')

    logging.info("stop")

'''
    with open(directory_path + "list.txt") as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content]

    my_set = set(content)

    with open(directory_path + 'your_file.txt', 'w') as f:
        for item in my_set:
            f.write("%s\n" % item)

'''