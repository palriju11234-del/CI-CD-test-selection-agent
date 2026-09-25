import pandas as pd

df = pd.read_csv('data/claims_all.csv')
s = df['claim'].astype(str).str.lower()
has_not = s.str.contains(r'\bnot\b', regex=True)

# Separate negated claims
# Separate negated claims by label
neg_true = df[has_not & (df["label"] == "true")]
neg_false = df[has_not & (df["label"] == "false")]
neg_uncertain = df[has_not & (df["label"] == "uncertain")]

print("\nOriginal negation distribution:")
print(
    df.loc[has_not, "label"].value_counts()
)

# Find largest negation class
target = max(
    len(neg_true),
    len(neg_false),
    len(neg_uncertain)
)

# Controlled oversampling
neg_true = neg_true.sample(
    target,
    replace=True,
    random_state=42
)

neg_false = neg_false.sample(
    target,
    replace=True,
    random_state=42
)

neg_uncertain = neg_uncertain.sample(
    target,
    replace=True,
    random_state=42
)

# Keep all non-negated claims
non_negated = df[~has_not]

# Combine
df_balanced = pd.concat([
    non_negated,
    neg_true,
    neg_false,
    neg_uncertain
])

# Shuffle
df_balanced = df_balanced.sample(
    frac=1,
    random_state=42
).reset_index(drop=True)

print("\nNew negation distribution:")
print(
    df_balanced.loc[
        df_balanced["claim"]
        .astype(str)
        .str.lower()
        .str.contains(r"\bnot\b", regex=True),
        "label"
    ].value_counts()
)

# Save
df_balanced.to_csv(
    "data/claims_balanced_negation.csv",
    index=False
)

print("\nSaved:")
print("data/claims_balanced_negation.csv")
print("Rows:", len(df_balanced))


print("New distribution for 'not':")
s_new = df_balanced['claim'].astype(str).str.lower()
print(df_balanced[s_new.str.contains(r'\bnot\b', regex=True)]['label'].value_counts())

df_balanced.to_csv(
    "data/claims_balanced_negation.csv",
    index=False
)

print("\nSaved:")
print("data/claims_balanced_negation.csv")
print(f"Rows: {len(df_balanced)}")

df = pd.read_csv("data/claims_balanced_negation.csv")

s = df["claim"].astype(str).str.lower()
has_not = s.str.contains(r"\bnot\b", regex=True)

print("\nNEGATION LABEL DISTRIBUTION:")
print(df.loc[has_not, "label"].value_counts())

print("\nTOTAL LABEL DISTRIBUTION:")
print(df["label"].value_counts())