import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from app.ml.dataset import load_dataset
from app.ml.vectorizer import create_vectorizer


def main():
    # Load dataset
    X, y = load_dataset()

    # Convert text to vectors
    vectorizer = create_vectorizer()
    X_vectors = vectorizer.fit_transform(X)

    # Split into training and testing data
    X_train, X_test, y_train, y_test = train_test_split(
        X_vectors,
        y,
        test_size=0.2,
        random_state=42
    )

    print("Training samples:", X_train.shape[0])
    print("Testing samples :", X_test.shape[0])

    # Create the model
   

    model = LinearSVC(
        class_weight="balanced",
        C=1.0
    )

    # Train the model
    model.fit(X_train, y_train)

    # Save the model and vectorizer
    os.makedirs("app/models", exist_ok=True)

    joblib.dump(model, "app/models/model.joblib")
    joblib.dump(vectorizer, "app/models/vectorizer.joblib")

    print("\n✅ Model saved successfully!")

    from sklearn.metrics import accuracy_score, classification_report

    # Make predictions on the test set
    y_pred = model.predict(X_test)

    print("\nPredictions:")
    print(y_pred)

    print("\nActual Labels:")
    print(list(y_test))

    # Accuracy
    accuracy = accuracy_score(y_test, y_pred)

    print(f"\nAccuracy: {accuracy:.2f}")

    # Detailed report
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    print("\n🎉 Model training completed!")


if __name__ == "__main__":
    main()
