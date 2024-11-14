# app.py
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# Title and description
st.title("Basic Streamlit App for Linear Regression")
st.write("This app lets you input data and see a simple linear regression.")

# Sidebar input
st.sidebar.header("Input Parameters")
def user_input_features():
    x_value = st.sidebar.slider("Input X", 0, 100, 25)
    return {"X": x_value}

input_data = user_input_features()
X = np.array([input_data["X"]]).reshape(-1, 1)

# Sample Data
np.random.seed(0)
x_sample = np.random.rand(100, 1) * 100
y_sample = 3 * x_sample + np.random.randn(100, 1) * 10 + 5

# Model Training
model = LinearRegression()
model.fit(x_sample, y_sample)

# Prediction
prediction = model.predict(X)
st.write(f"Predicted value for Y when X={X.flatten()[0]} is {prediction.flatten()[0]:.2f}")

# Plotting
plt.figure(figsize=(10, 5))
plt.scatter(x_sample, y_sample, color="blue", label="Data")
plt.plot(x_sample, model.predict(x_sample), color="red", linewidth=2, label="Regression Line")
plt.scatter(X, prediction, color="green", label="Prediction", marker="x", s=100)
plt.xlabel("X")
plt.ylabel("Y")
plt.legend()
st.pyplot(plt)
