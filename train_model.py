# train_model.py
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# ✅ Sample dataset
data = {
    'skills': ['programming', 'writing', 'design', 'math', 'biology'],
    'interests': ['AI', 'journalism', 'art', 'engineering', 'medicine'],
    'score': [85, 70, 75, 90, 80],
    'career': ['Software Engineer', 'Content Writer', 'Graphic Designer', 'Mechanical Engineer', 'Doctor']
}

df = pd.DataFrame(data)

# ✅ Encode categorical features to numeric values
df['skills'] = df['skills'].astype('category').cat.codes
df['interests'] = df['interests'].astype('category').cat.codes

# ✅ Feature matrix and target column
X = df[['skills', 'interests', 'score']]
y = df['career']

# ✅ Train model
model = RandomForestClassifier()
model.fit(X, y)

# ✅ Save model
joblib.dump(model, 'career_model.pkl')
print("✅ Model saved as career_model.pkl")
