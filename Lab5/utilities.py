import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import confusion_matrix

def classify_svm(df, test_size=0.5, c_param=1.0, kernel='rbf'):
    """
    Classifies data using an SVM with configurable parameters.

    Args:
        df (pd.DataFrame): The input DataFrame.
        test_size (float, optional): Proportion of the dataset used for testing. Defaults to 0.2.
        c_param (float, optional): Regularization parameter C for the SVM. Defaults to 1.0.
        kernel (str, optional): Kernel type to be used by the SVM. Defaults to 'rbf'.

    Returns:
        Accuracy: Overall accuracy score on the test set.
        Confusion Matrix (TP, FP, TN, FN): Breakdown of true positives, false positives, true negatives, and false negatives.
        Model: The trained SVM model pipeline.
        X_test: Test data features.
        Y_test: True labels for the test data.
    """

    X = df.drop(columns=["label"])
    y = df["label"]

    # Most of this function was coded with help of ChatGPT
    # Prompt: Help me to build a classifier model for a dataset that has numerical and categorical data

    # Identify categorical and numerical columns in the dataset
    categorical_cols = X.select_dtypes(include=['object']).columns.tolist()
    numerical_cols = X.select_dtypes(exclude=['object']).columns.tolist()

    # Pipeline for numerical features:
    # 1. Impute missing values with the median.
    # 2. Scale features to have zero mean and unit variance.
    numerical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    # Transformer for categorical features:
    # 1. One-hot encode categorical variables; unknown categories during transform will be ignored.
    categorical_transformer = OneHotEncoder(handle_unknown='ignore')

    # Combine numerical and categorical transformers into one preprocessor
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numerical_transformer, numerical_cols),
            ('cat', categorical_transformer, categorical_cols)
        ])

    # Create a pipeline that first preprocesses the data then fits an SVM classifier
    model = Pipeline(steps=[('preprocessor', preprocessor),
                            ('classifier', SVC(random_state=42, C=c_param, kernel=kernel))])

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)

    # Train the model on the training data
    model.fit(X_train, y_train)
    # Predict labels for the test data
    y_pred = model.predict(X_test)
    # Compute the accuracy of the model on the test set
    accuracy = accuracy_score(y_test, y_pred)

    # Compute the confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    TN, FP, FN, TP = cm[0][0], cm[0][1], cm[1][0], cm[1][1]

    return accuracy, TP, FP, TN, FN, model, X_test, y_test
