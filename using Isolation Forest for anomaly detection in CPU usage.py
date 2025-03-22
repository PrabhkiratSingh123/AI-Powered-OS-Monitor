from sklearn.ensemble import IsolationForest
import numpy as np

# Sample CPU usage data (Replace with actual data collection)
cpu_usage_data = np.array([20, 22, 21, 19, 85, 23, 20, 22, 95]).reshape(-1, 1)

# Train the anomaly detection model
model = IsolationForest(contamination=0.1)
model.fit(cpu_usage_data)

# Predict anomalies
predictions = model.predict(cpu_usage_data)
anomalies = cpu_usage_data[predictions == -1]

print("Anomalous CPU Usage:", anomalies)
