import streamlit as st
import tensorflow as tf
from tensorflow.keras.models import load_model
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
import pickle
import pandas as pd
import numpy as np

# Load the trained model
model = tf.keras.models.load_model('model.h5')

## load the encoder and scalar
with open('onehot_encoder_geo.pkl', 'rb') as file:
    onehot_encoder_geo = pickle.load(file)

with open('label_encoder_gender.pkl', 'rb') as file:
    label_encoder_gender = pickle.load(file)

with open('scalar.pkl', 'rb') as file:
    scalar = pickle.load(file)


## Streamlit app
st.title('Customer Churn Prediction')

#User input
geography = st.selectbox('Geography', onehot_encoder_geo.categories_[0])
gender = st.selectbox('Gender', label_encoder_gender.classes_)
age = st.slider('Age', 18, 92)
balance = st.number_input('Balance')
credit_score = st.number_input('Credit Score')
estimated_salary = st.number_input('Estimated Salary')
tenure = st.slider('Tenure', 0, 10)
num_of_products = st.slider('Number of products', 1, 4)
has_cr_card = st.selectbox('Has Credit Card', [0, 1])
is_active_number = st.selectbox('Is Active Number', [0, 1])


# Prepare the input data
input_data = pd.DataFrame({
    'CreditScore': [credit_score],
    # 'Geography': [label_encoder_gender.transform([gender])[0]]
    'Gender': [label_encoder_gender.transform([gender])[0]],
    'Age': [age],
    'Tenure': [tenure],
    'Balance': [balance],
    'NumOfProducts': [num_of_products],
    'HasCrCard': [has_cr_card],
    "IsActiveMember": [is_active_number],
    'EstimatedSalary': [estimated_salary]
})

# One-hot encoder 'Geography'
geo_encode = onehot_encoder_geo.transform([[geography]]).toarray()
geo_encode_df = pd.DataFrame(geo_encode, columns=onehot_encoder_geo.get_feature_names_out(['Geography']))

# Combine one-hot encoder columns with input data
input_data = pd.concat([input_data.reset_index(drop=True), geo_encode_df], axis=1)

# Scale the input data
input_data_scaled = scalar.transform(input_data)

# Prediction churn 
prediction = model.predict(input_data_scaled)
prediction_proba = prediction[0][0]


st.write(prediction_proba)
if prediction_proba > 0.5:
    st.write('The customer is likely to churn.')
else:
    st.write('The customer is not likely to churn.')


