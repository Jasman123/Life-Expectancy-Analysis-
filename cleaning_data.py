import numpy as np
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "Life Expectancy Data.csv"
df = pd.read_csv(DATA_PATH)
df.columns = df.columns.str.strip()

TARGET = "Life expectancy"

df_numeric = df.select_dtypes(include="number")

corr = df_numeric.corr()[TARGET]
selected_features = corr[abs(corr) >= 0.5].index.tolist()

print("Selected features:", selected_features)
df_model = df[selected_features + ["Country", "Year", "Status"]]

critical_cols = ["Adult Mortality", TARGET, "BMI"]
df_model = df_model.dropna(subset=critical_cols)

mean_fill_cols = ["Income composition of resources", "Schooling"]

for col in mean_fill_cols:
    df_model[col] = df_model[col].astype(float)
    df_model[col] = df_model[col].fillna(df_model[col].mean())

if "HIV/AIDS" in df_model.columns:
    q98 = df_model["HIV/AIDS"].quantile(0.98)
    df_model = df_model[df_model["HIV/AIDS"] < q98]

categorical_cols = ["Country", "Status"]
df_final = pd.get_dummies(
    df_model,
    columns=categorical_cols,
    drop_first=True
)

df_model = df_model.dropna()

print("\nMissing values after cleaning:")
print(df_model.isnull().sum())

OUTPUT_FILE = BASE_DIR / "life_expectancy_cleaned.csv"


df_final.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

