import pickle
import pandas as pd
from pipeline import build_pipeline


# Load cleaned dataset
df = pd.read_csv("../Data/processed/final_model_data.csv")

X = df.drop("Final_Price", axis=1)
y = df["Final_Price"]

pipeline = build_pipeline()
pipeline.fit(X, y)

pickle.dump(
    pipeline,
    open("house_price_pipeline.pkl", "wb")
)

print("Pipeline trained and saved!")
