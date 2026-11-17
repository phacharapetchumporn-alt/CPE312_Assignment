from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import joblib, os

data = fetch_california_housing(as_frame=False)
X, y = data.data, data.target

Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(Xtr, ytr)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_dir = os.path.join(BASE_DIR, "model")
os.makedirs(model_dir, exist_ok=True)
model_path = os.path.join(model_dir, "model.pkl")
joblib.dump(model, model_path)
print(f"บันทึกโมเดลเรียบร้อยที่ {model_path}")
