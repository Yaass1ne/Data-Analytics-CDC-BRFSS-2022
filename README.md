Lifestyle Patterns vs. Disease Rates
Streamlit Dashboard & Full Data Pipeline
(CDC BRFSS 2022)

Contributors
- Yassine Yahyaoui
- Bechir Ben Tekfa
- Mohamed Yassine Ezzaouia

--------------------------------------------------
1 · Project Overview
We analyse how lifestyle variables (BMI, exercise, etc.) relate to chronic‑disease indicators (diabetes, heart disease) using the 2022 Behavioral Risk Factor Surveillance System (BRFSS) micro‑data.

Repo layout:
.
├── data/
│   ├── brfss2022_enriched.csv       (cleaned data)
│   └── diabetes_logit_coeffs.csv    (model β‑coeffs)
├── notebooks/
│   └── BRFSS_Data_Pipeline.ipynb    (ETL + EDA)
├── dashboard/
│   └── streamlit_app.py             (web app)
├── requirements.txt
└── README.txt   (this file)

--------------------------------------------------
2 · Quick‑start (local)

To run this repo you need to:
1. First run the notebook to create the enriched CSV and model coefficients.
2. Install dependencies:
   pip install -r requirements.txt
3. Run the Streamlit app:
   streamlit run dashboard/streamlit_app.py
4. Wait for the dashboard to fully execute, then start exploring!

Example session:

git clone https://github.com/<your-org>/lifestyle-disease-analysis.git
cd lifestyle-disease-analysis
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
jupyter lab notebooks/BRFSS_Data_Pipeline.ipynb   # run all
streamlit run dashboard/streamlit_app.py

--------------------------------------------------
3 · Git & GitHub Workflow
add remote      : git remote add origin https://github.com/<your-org>/lifestyle-disease-analysis.git
first push      : git add . && git commit -m "Initial commit" && git push -u origin main
later updates   : git add <files> && git commit -m "<msg>" && git push

Large files: if any CSV >100 MB, enable Git LFS (git lfs install; git lfs track "*.csv").

--------------------------------------------------
4 · Deploy on Streamlit Cloud
1. Push repo to GitHub.
2. Create new app on Streamlit Cloud, main file = dashboard/streamlit_app.py.
3. requirements.txt must list:
   pandas
   numpy
   streamlit
   seaborn
   scikit-learn
   matplotlib
4. Click Deploy (first build ~2 min).

--------------------------------------------------
5 · Screenshots to include in report
Dashboard_Overview.png   – Overview tab
Dashboard_Heatmap.png    – Risk Heat‑Map tab
Dashboard_Predictor.png  – Risk Predictor tab
Dashboard_Clusters.png   – Cluster Explorer plot
Dashboard_Data.png       – Data tab

--------------------------------------------------
6 · License & Data Source
Code: MIT License
Data: CDC BRFSS 2022 (public domain)
https://www.cdc.gov/brfss/annual_data/annual_2022.html
