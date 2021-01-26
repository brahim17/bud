import releve.bnp_releve as releve
import tools.yamlConfig as yc

directory_path = yc.get_path()

if __name__ == '__main__':

    df_bnp = releve.df_extract_bnp_releve(None)
    df_bnp.to_csv(directory_path + "bnp-raw-1.5.csv")
