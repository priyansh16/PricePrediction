# 🏠 Swedish Property Price Analytics
**An End-to-End Machine Learning Pipeline: From Selenium-based Extraction to XGBoost Modeling.**

This project demonstrates a complete ML lifecycle designed to provide data-driven insights into the Swedish housing market. It addresses the challenge of data accessibility by engineering a custom scraper and delivering a predictive model for property valuation.

---

### 🛠️ Tech Stack
* **Data Acquisition:** Selenium (WebDriver)
* **Data Processing:** Pandas, NumPy, Scikit-Learn
* **Modeling:** XGBoost Regression
* **Visualization:** Matplotlib, Seaborn
* **Infrastructure:** AWS (In-Progress), Docker, Git (Version Control)

---

### 🚀 The ML Lifecycle



1.  **Data Acquisition:** Developed an automated **Selenium-based pipeline** to aggregate real-time property listings from Swedish real-estate platforms, effectively bypassing the lack of public APIs.
2.  **Feature Engineering:** * Implemented robust **categorical encoding** for Swedish municipalities.
    * Engineered logic for handling missing values and outlier detection for specific Swedish property metrics (e.g., *boarea*, *biarea*, *tomtarea*).
3.  **Exploratory Data Analysis (EDA):** Identified key price drivers and regional trends using statistical distributions, correlation heatmaps, and geospatial insights.
4.  **Model Training:** Optimized an **XGBoost Regressor** to handle the non-linear relationships inherent in financial and geographical data, ensuring high-fidelity valuation predictions.
5.  **Deployment (In-Progress):** Architecting a scalable **AWS-based inference API** and **CI/CD** pipelines to ensure automated model retraining and production-grade delivery.

---

### 📂 Repository Structure
* `Scripts/` : Production-grade Selenium scrapers and data cleaning modules.
* `Notebooks/` : Detailed Jupyter Notebooks covering EDA and model experimentation.
* `Data/` : Directory for extracted raw datasets and final cleaned versions.
* `FinalModel.pkl` : The serialized **XGBoost model** ready for production inference.

---

### 📈 Future Roadmap
- [ ] **CI/CD Integration:** Implementing GitHub Actions for automated testing and deployment.
- [ ] **AWS Deployment:** Hosting the inference engine on **AWS (EC2/Lambda)** to provide a scalable REST API.
- [ ] **Multimodal Expansion:** Utilizing property images for price refinement through Computer Vision.

---

### 🤝 Connect
Feedback and contributions are welcome!
* **Issues:** [Report here](https://github.com/priyansh16/PricePrediction/issues)
* **LinkedIn:** [Priyansh Gupta](https://www.linkedin.com/in/pggupta/)

---

### 📄 License
This project is licensed under the [MIT License](https://opensource.org/license/mit).