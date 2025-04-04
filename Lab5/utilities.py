import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from Lab5.ingestion import *
from sklearn.metrics import confusion_matrix


def classify_svm(df, test_size=0.2, c_param=1.0, kernel='linear'):
    """
    Classifies data using an SVM with configurable parameters.

    Args:
        df (pd.DataFrame): The input DataFrame.
        test_size (float, optional): The proportion of the dataset to include in the test split. Defaults to 0.2.
        c_param (float, optional): Regularization parameter C of the SVM. Defaults to 1.0.
        kernel (str, optional): Specifies the kernel type to be used in the algorithm. Defaults to 'linear'.
    Returns:
        Accuracy
        Confusion Matrix (broken into TP, FP, TN, FN)
        Model
        X_test
        Y_test
    """

    X = df.drop(columns=["label"])
    y = df["label"]

    categorical_cols = X.select_dtypes(include=['object']).columns.tolist()
    numerical_cols = X.select_dtypes(exclude=['object']).columns.tolist()

    numerical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    categorical_transformer = OneHotEncoder(handle_unknown='ignore')

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numerical_transformer, numerical_cols),
            ('cat', categorical_transformer, categorical_cols)
        ])

    model = Pipeline(steps=[('preprocessor', preprocessor),
                            ('classifier', SVC(random_state=42, C=c_param, kernel=kernel))])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    # Compute confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    TN, FP, FN, TP = cm[0][0], cm[0][1], cm[1][0], cm[1][1]

    return accuracy, TP, FP, TN, FN, model, X_test, y_test
