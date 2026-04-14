import pandas as pd
import re
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# Load dataset
df = pd.read_csv("dataset.csv")

print("Columns:", df.columns)

# ✅ Step 1: Remove rows with missing Title
df = df.dropna(subset=['Title'])

# ✅ Step 2: Fill missing text fields with empty string
df['Skills'] = df['Skills'].fillna('')
df['Responsibilities'] = df['Responsibilities'].fillna('')
df['Keywords'] = df['Keywords'].fillna('')

# ✅ Step 3: Combine text columns
df['text'] = df['Skills'] + " " + df['Responsibilities'] + " " + df['Keywords']

# Clean text
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'[^a-z ]', '', text)
    return text

df['cleaned'] = df['text'].apply(clean_text)

# Features
tfidf = TfidfVectorizer(max_features=3000)
X = tfidf.fit_transform(df['cleaned'])

# Labels (job roles)
y = df['Title']

# Train model
model = MultinomialNB()
model.fit(X, y)

# Save model
pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(tfidf, open("tfidf.pkl", "wb"))

print("✅ Model trained successfully!")