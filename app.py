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
        
        log_data = df.copy()
        log_data["prediction"] = round(prediction, 2)
        log_data["timestamp"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        log_file = os.path.join(BASE_DIR, "model_logs.csv")
        # Append to CSV, only write header if file doesn't exist
        log_data.to_csv(log_file, mode='a', index=False, header=not os.path.exists(log_file))
        
        return jsonify({"value": round(prediction, 2)})
    except Exception as e:
        return jsonify({"error": str(e)})
    
    
@app.route("/logs")
def view_logs():
    try:
        log_file = os.path.join(BASE_DIR, "model_logs.csv")
        if os.path.exists(log_file):
            df_logs = pd.read_csv(log_file)
            # Return as HTML table for a quick "dashboard"
            return df_logs.tail(20).to_html(classes='table table-striped')
        return "No logs found yet."
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=3000)
