from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd
import sys
import os
import datetime

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR, 'model'))
model_path = os.path.join(BASE_DIR, "model", "house_price_pipeline.pkl")
# Load pipeline
pipeline = pickle.load(open(model_path, "rb"))

@app.route("/")
def root():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        
        df = pd.DataFrame([{
        "Municipality": data["Municipality"],
        "Living_area": float(data["Living_area"]),
        "Built_on": data["Built_On"],
        "House_type": data["House_type"],
        "Lift": data["Lift"] ,
        "Balcony": data["Balcony"]
        }])
        
        prediction =  pipeline.predict(df)[0]
        
        #Logging
        log_data = df.copy()
        log_data["Prediction"] = round(prediction, 2)
        log_data["Timestamp"] = datetime.datetime.now()
        
        log_file = os.path.join(BASE_DIR, "model_logs.csv")
        # Append to CSV, only write header if file doesn't exist
        log_data.to_csv(
            log_file, 
            mode='a',
            index=False,
            header=not os.path.exists(log_file),
            encoding="utf-8"
            )
        
        return jsonify({"value": round(prediction, 2)})
    except Exception as e:
        return jsonify({"error": str(e)})
    
    
# ------------------------
# Monitoring Dashboard Page
# ------------------------

@app.route("/monitoring")
def monitoring():
    return render_template("monitoring.html")


@app.route("/monitoring-data")
def monitoring_data():

    log_file = os.path.join(BASE_DIR, "model_logs.csv")

    if not os.path.exists(log_file):
        return jsonify({})

    df = pd.read_csv(log_file, encoding="utf-8")
    
    if df.empty:
        print('empty file')
        return jsonify({})

    df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")
    df["date"] = df["Timestamp"].dt.date

    # Prediction count per day
    usage = df.groupby("date").size()

    # Average predicted price by date and house type
    avg_by_type = (df.groupby(["date", "House_type"])["Prediction"].mean().reset_index())
    
    pivot_avg = avg_by_type.pivot(
        index = "date",
        columns = "House_type",
        values = "Prediction"
    ).fillna(method="ffill")
    
    pivot_avg = pivot_avg.sort_index()
    
    # Municipality distribution
    municipality_counts = df["Municipality"].value_counts()
    print(f"usage_dates: {usage.index.astype(str).tolist()}, usage_counts: {usage.tolist()}, avg_dates:{pivot_avg.index.astype(str).tolist()}")
    print(f"avg_values: {pivot_avg.to_dict(orient = "list")}, municipalities: {municipality_counts.index.tolist()}, municipality_counts: {municipality_counts.tolist()}")
    print(f"recent_logs: {df.tail(5).to_dict(orient="records")}")
    
    return jsonify({
        "usage_dates": usage.index.astype(str).tolist(),
        "usage_counts": usage.tolist(),
        
        "avg_dates": pivot_avg.index.astype(str).tolist(),
        "avg_values": pivot_avg.to_dict(orient = "list"),
        
        "municipalities": municipality_counts.index.tolist(),
        "municipality_counts": municipality_counts.tolist(),
        "recent_logs": df.tail(5).to_dict(orient="records")
    })


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=3000)
