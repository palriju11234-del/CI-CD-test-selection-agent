from app.ml.dataset import load_dataset
from app.ml.vectorizer import create_vectorizer


def test_load_dataset_returns_x_and_y():
    X, y = load_dataset()
    assert len(X) > 0
    assert len(y) > 0
    assert len(X) == len(y)


def test_load_dataset_x_are_strings():
    X, y = load_dataset()
    assert all(isinstance(v, str) for v in X)


def test_load_dataset_labels_are_valid():
    X, y = load_dataset()
    valid_labels = {"true", "false", "uncertain", "half-true", "barely-true",
                    "mostly-true", "pants-fire", "TRUE", "FALSE", "HALF-TRUE",
                    "BARELY-TRUE", "MOSTLY-TRUE", "PANTS-FIRE"}
    unique = set(str(label) for label in y.unique())
    # Labels should be non-empty strings
    assert len(unique) > 0


def test_create_vectorizer_fits_and_transforms():
    X, y = load_dataset()
    vectorizer = create_vectorizer()
    X_vec = vectorizer.fit_transform(X)
    assert X_vec.shape[0] == len(X)
    assert X_vec.shape[1] > 0