import pandas as pd


def pull_and_clean_data():
    df1 = pd.read_csv("Data/Credit_card.csv")
    df2 = pd.read_csv("Data/Credit_card_label.csv")

    df = pd.merge(df1, df2, on="Ind_ID", how="inner")
    df = df.drop(columns=["Ind_ID"])

    # Make unemployed people have a value of 1000 to be better shown in the graph (originally it was 365,000)
    df.loc[df["Employed_days"] > 0, "Employed_days"] = 1000

    # Keep all positive records (credit card rejections)
    df_positive = df[df["label"] == 1]

    # Randomly sample and keep 700 accepted applications
    # This makes the dataset 4:1 instead of 12:1 in its original state
    df_negative = df[df["label"] == 0].sample(n=700, random_state=42)

    # Concatenate the positives and negatives and reset the index
    df_balanced = pd.concat([df_positive, df_negative]).reset_index(drop=True)

    return df_balanced
