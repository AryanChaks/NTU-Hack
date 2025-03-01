# -*- coding: utf-8 -*-
"""Next_Calibration.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/13Bt561Xy6UhWOqsLpJ-cPlXzbSLirHW_
"""

import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.model_selection import train_test_split
import joblib
import matplotlib.pyplot as plt

# Load preprocessed dataset
df = pd.read_csv("Processed_Bosch_Dataset.csv")

# Select relevant features
features = ["Days_Since_Last_Calibration", "Days_Until_Next_Calibration", "Calibration_Interval_Years"]
target = "Days_Until_Next_Calibration"  # Predict when the next calibration is due

# Load the scaler from 'scaler.pkl'
scaler = joblib.load("scaler.pkl")

# Apply the same transformation to maintain consistency
features = ["Calibration_Interval_Years", "Months_Remaining", "Days_Since_Last_Calibration", "Days_Until_Next_Calibration"]
df[features] = scaler.transform(df[features])  # Use transform() instead of fit_transform()

# Convert data to supervised learning format
def create_sequences(data, target_col, seq_length=5):
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data.iloc[i:i+seq_length].values)
        y.append(data.iloc[i+seq_length][target_col])
    return np.array(X), np.array(y)

# Convert to LSTM input format
X, y = create_sequences(df[features], target)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=False)

# Build LSTM Model
model = Sequential([
    LSTM(50, return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[2])),
    Dropout(0.2),
    LSTM(50, return_sequences=False),
    Dropout(0.2),
    Dense(25, activation="relu"),
    Dense(1)  # Predict next calibration date
])

# Compile Model
model.compile(optimizer="adam", loss="mse", metrics=["mae"])

# Train Model
history = model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=50, batch_size=16, verbose=1)

# Evaluate Model
loss, mae = model.evaluate(X_test, y_test)
print(f"\n Model Evaluation → Loss: {loss:.4f}, MAE: {mae:.4f}")

# Plot training vs validation loss
plt.plot(history.history["loss"], label="Training Loss")
plt.plot(history.history["val_loss"], label="Validation Loss")
plt.legend()
plt.title("LSTM Training vs Validation Loss")
plt.show()

# Select a random unseen test sample
random_sample = X_test[5].reshape(1, X_test.shape[1], X_test.shape[2])

# Predict the next calibration date
predicted_days = model.predict(random_sample)

# Convert prediction back to original scale
predicted_original = scaler.inverse_transform([[0, 0, predicted_days[0][0], 0]])[:, 2]

print(f"\n🔹 Predicted Days Until Next Calibration: {predicted_original[0]:.2f}")

# Make Predictions
y_pred = model.predict(X_test)

# Convert Predictions Back to Original Scale

# Create an array with the correct number of features (4)
num_samples = y_pred.shape[0]  # Get the number of samples in y_pred
transformed_data = np.zeros((num_samples, 4))  # Initialize an array with zeros

# Fill the relevant column with the predictions
transformed_data[:, 3] = y_pred.flatten()  # Assuming 'Days_Until_Next_Calibration' is the 4th column (index 3)

# Apply inverse_transform
y_pred_original = scaler.inverse_transform(transformed_data)[:, 3]  # Extract the predicted 'Days_Until_Next_Calibration'

# Save Predictions
df_predictions = pd.DataFrame({"Actual_Days_Until_Next_Calibration": y_test, "Predicted_Days_Until_Next_Calibration": y_pred_original})
df_predictions.to_csv("LSTM_Predictions.csv", index=False)

# Save Model
model.save("calibration_forecast_lstm.h5")

print("\n LSTM Model Training Complete & Saved!")