import pandas as pd
import pickle as pk
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
import shap  # Import SHAP

import warnings
warnings.filterwarnings("ignore")

data_pose = pd.read_csv(r'C:\research_paper\research paper\yoga-pose-detection-correction-main\csv_files\poses_data_pose.csv')
print("Dataset shape:", data_pose.shape)
features = data_pose.drop(["pose"], axis=1)
target = data_pose[["pose"]]

X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2)

data_all_pose_model = RandomForestClassifier()
data_all_pose_model.fit(X_train, y_train)
print(classification_report(y_test, data_all_pose_model.predict(X_test)))

# Save the model
pk.dump(data_all_pose_model, open(f"./models/poses.model", "wb"))

# Calculate SHAP values
explainer = shap.TreeExplainer(data_all_pose_model)
shap_values = explainer.shap_values(X_test)

# Save the SHAP values for further analysis
with open('./models/shap_values.pkl', 'wb') as f:
    pk.dump(shap_values, f)