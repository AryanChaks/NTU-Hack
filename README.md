Feature/anomaly-detection Branch (README.md)
📍 Purpose:
This branch implements Autoencoder-based Anomaly Detection for identifying faulty calibrations.

📂 Directory Structure:
src/
│── anomaly_detection.py    # Autoencoder Training
│── detect_anomalies.py     # Anomaly Detection Script
models/
│── autoencoder.h5          # Saved Autoencoder Model
notebooks/
│── Anomaly_Detection.ipynb # Jupyter Notebook for Experiments



develop Branch (README.md)
📍 Purpose:
This branch contains ongoing development, where all new features are merged before reaching main.

📂 Current Features in Development:

 LSTM Model for Predictive Calibration
 Autoencoder for Anomaly Detection
 NLP-Based Compliance Reports
 Streamlit Dashboard



 feature/lstm Branch (README.md)
📍 Purpose:
This branch contains LSTM-based Predictive Calibration Model for forecasting tool maintenance schedules.

📂 Directory Structure:
src/
│── lstm_training.py         # LSTM Model Training
│── lstm_prediction.py       # LSTM Model Inference
models/
│── lstm_model.h5            # Saved LSTM Model
notebooks/
│── LSTM_Experiments.ipynb   # Jupyter Notebook for Model Testing
