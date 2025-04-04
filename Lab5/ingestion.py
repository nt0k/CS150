import pandas as pd

def pull_and_clean_data():
    df1 = pd.read_csv("/Users/admin/PycharmProjects/CS150/Lab5/Data/Credit_card.csv")
    df2 = pd.read_csv("/Users/admin/PycharmProjects/CS150/Lab5/Data/Credit_card_label.csv")

    df = pd.merge(df1, df2, on="Ind_ID", how="inner")
    df = df.drop(columns=["Ind_ID"])
    df.loc[df["Employed_days"] > 0, "Employed_days"] = 1000

    # Keep all positive records (label = 1)
    df_positive = df[df["label"] == 1]
    # Randomly sample 175 negative records (label = 0)
    df_negative = df[df["label"] == 0].sample(n=175, random_state=42)

    # Concatenate the positives and negatives and reset the index
    df_balanced = pd.concat([df_positive, df_negative]).reset_index(drop=True)


    return df_balanced
