import streamlit as st
import pandas as pd
import joblib

# Load trained model
model = joblib.load("best_mushroom_model.pkl")

# Define all possible features (excluding 'class') from the dataset
features = {
    "cap-shape": ['bell', 'conical', 'convex', 'flat', 'knobbed', 'sunken'],
    "cap-surface": ['fibrous', 'grooves', 'scaly', 'smooth'],
    "cap-color": ['brown', 'buff', 'cinnamon', 'gray', 'green', 'pink', 'purple', 'red', 'white', 'yellow'],
    "bruises": ['bruises', 'no'],
    "odor": ['almond', 'anise', 'creosote', 'fishy', 'foul', 'musty', 'none', 'pungent', 'spicy'],
    "gill-attachment": ['attached', 'descending', 'free', 'notched'],
    "gill-spacing": ['close', 'crowded', 'distant'],
    "gill-size": ['broad', 'narrow'],
    "gill-color": ['black', 'brown', 'buff', 'chocolate', 'gray', 'green', 'orange', 'pink', 'purple', 'red', 'white', 'yellow'],
    "stalk-shape": ['enlarging', 'tapering'],
    "stalk-root": ['bulbous', 'club', 'cup', 'equal', 'rhizomorphs', 'rooted', 'missing'],
    "stalk-surface-above-ring": ['fibrous', 'scaly', 'silky', 'smooth'],
    "stalk-surface-below-ring": ['fibrous', 'scaly', 'silky', 'smooth'],
    "stalk-color-above-ring": ['brown', 'buff', 'cinnamon', 'gray', 'orange', 'pink', 'red', 'white', 'yellow'],
    "stalk-color-below-ring": ['brown', 'buff', 'cinnamon', 'gray', 'orange', 'pink', 'red', 'white', 'yellow'],
    "veil-type": ['partial'],  # Only one value in dataset
    "veil-color": ['brown', 'orange', 'white', 'yellow'],
    "ring-number": ['none', 'one', 'two'],
    "ring-type": ['cobwebby', 'evanescent', 'flaring', 'large', 'none', 'pendant', 'sheathing', 'zone'],
    "spore-print-color": ['black', 'brown', 'buff', 'chocolate', 'green', 'orange', 'purple', 'white', 'yellow'],
    "population": ['abundant', 'clustered', 'numerous', 'scattered', 'several', 'solitary'],
    "habitat": ['grasses', 'leaves', 'meadows', 'paths', 'urban', 'waste', 'woods']
}

# Load encoders for consistency with training
encoders = {col: pd.Series(vals).astype('category').cat.categories for col, vals in features.items()}

# Title
st.title("🍄 Mushroom Classification App")
st.write("Predict whether a mushroom is **poisonous or edible** based on its features.")

# Sidebar form
with st.sidebar.form("input_form"):
    st.subheader("Enter Mushroom Features")
    input_data = {}
    for feature, options in features.items():
        input_data[feature] = st.selectbox(feature.replace("-", " ").title(), options)

    submitted = st.form_submit_button("Predict")

if submitted:
    # Create DataFrame for input
    input_df = pd.DataFrame([input_data])

    # Encode the input using same categories as training
    for col in input_df.columns:
        input_df[col] = pd.Categorical(input_df[col], categories=encoders[col]).codes

    # Predict
    prediction = model.predict(input_df)[0]

    # Output result
    result = "🍄 Poisonous" if prediction == 1 else "✅ Edible"
    st.subheader("Prediction:")
    st.success(result)
