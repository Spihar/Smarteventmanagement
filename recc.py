import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MultiLabelBinarizer
import pickle

# Simulated dataset
data = {
    'department': ['AI', 'DS', 'Cybersecurity', 'EEE', 'AI', 'DS', 'Mech', 'Civil', 'AIML', 'IoT', 'BCT', 'ML', 'AI Robotics'],
    'events': [
        ['AI Conference', 'ML Hackathon', 'Deep Learning Bootcamp'],
        ['Data Science Summit', 'ML Hackathon'],
        ['Cyber Drill', 'Ethical Hacking Workshop'],
        ['Circuit Design', 'Power Systems'],
        ['NLP Talk', 'AI Conference'],
        ['Big Data Bootcamp', 'DS Workshop'],
        ['AutoCAD Workshop', 'Mech Expo'],
        ['Surveying Workshop', 'Civil Tech Meet'],
        ['ML Hackathon', 'NLP Talk'],
        ['IoT Summit', 'Smart Devices Fair'],
        ['Cloud Tech', 'BCT Networking'],
        ['ML Hackathon', 'Big Data Bootcamp'],
        ['AI Robotics Expo', 'Machine Vision Talk']
    ]
}

df = pd.DataFrame(data)
print(df)

# Encode events
mlb = MultiLabelBinarizer()
event_features = mlb.fit_transform(df['events'])
print(event_features)
event_df = pd.DataFrame(event_features, columns=mlb.classes_)

# Combine features and labels
X = event_df
y = df['department']

# Train the model
model = RandomForestClassifier()
model.fit(X, y)

# Save model and event encoder
pickle.dump(model, open('event_recommendation_model.pkl', 'wb'))
pickle.dump(mlb, open('event_mlb.pkl', 'wb'))
