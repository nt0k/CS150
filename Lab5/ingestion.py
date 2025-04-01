import pandas as pd

def pull_and_clean_data():
    df1 = pd.read_csv("/Users/admin/PycharmProjects/CS150/Lab5/Data/Credit_card.csv")
    df2 = pd.read_csv("/Users/admin/PycharmProjects/CS150/Lab5/Data/Credit_card_label.csv")

    df = pd.merge(df1, df2, on="Ind_ID", how="inner")
    df = df.drop(columns=["Ind_ID"])
    return df
