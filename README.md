
# Lifestyle Patterns vs. Disease Rates  
**Streamlit Dashboard & Full Data Pipeline**  
*(CDC BRFSS 2022)*  

**Contributors**  
- Yassine Yahyaoui  
- Bechir Ben Tekfa  
- Mohamed Yassine Ezzaouia  

---

## 1 · Project Overview  

We analyse how lifestyle variables (BMI, exercise, etc.) relate to chronic‑disease indicators (diabetes, heart disease) using the 2022 **Behavioral Risk Factor Surveillance System (BRFSS)** micro‑data.

<details>
<summary>Repository layout</summary>

```text
.
├── data/
│   ├── brfss2022_enriched.csv    # cleaned + engineered data
│   └── diabetes_logit_coeffs.csv # logistic‑regression β‑coeffs
│   └── brfss2022_clean
├── LLCP2022.XPT.zip
├── BRFSS_Data_Pipeline.ipynb # full ETL + EDA notebook
├── streamlit_app.py          # interactive web app
├── req.txt
└── README.md                
```
</details>

---

## 2 · Quick‑start (local)  

**To run this repo you need to:**

1. **First run the notebook** to create the enriched CSV *and* model coefficients.  
2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```  

3. **Run the Streamlit app**

   ```bash
   streamlit run dashboard/streamlit_app.py
   ```  

4. **Wait** for the dashboard to finish loading, then start exploring!

**Example session**

```bash
# clone repo
git clone https://github.com/<YOUR-ORG>/lifestyle-disease-analysis.git
cd lifestyle-disease-analysis

# (optional) create + activate venv
python -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate

# install deps
pip install -r requirements.txt

# generate data
jupyter lab BRFSS_Data_Pipeline.ipynb   # run all cells

# launch app
streamlit run streamlit_app.py
```

---

## 3 · Git & GitHub Workflow  

| Purpose | Command |
|---------|---------|
| **Add remote** | `git remote add origin https://github.com/<YOUR-ORG>/lifestyle-disease-analysis.git` |
| **First push** | `git add . && git commit -m "Initial commit" && git push -u origin main` |
| **Later updates** | `git add <files> && git commit -m "<msg>" && git push` |

> **Large files**    
> If any CSV exceeds **100 MB** (GitHub hard limit), enable Git LFS:  
> `git lfs install && git lfs track "*.csv" && git add .gitattributes <file>.csv`

---

## 4 · Deploy on Streamlit Cloud  

1. Push the repo to GitHub.  
2. Open <https://streamlit.io/cloud> → **New app**.  
3. Select repo & branch `main`, set **`dashboard/streamlit_app.py`** as the main file.  
4. Ensure `requirements.txt` contains:

   ```
   pandas
   numpy
   streamlit
   seaborn
   scikit-learn
   matplotlib
   ```

5. Click **Deploy** – first build takes ≈ 2 min.



## 5 · License & Data Source  

* **Code:** MIT License  
* **Data:** CDC BRFSS 2022 (public domain) – <https://www.cdc.gov/brfss/annual_data/annual_2022.html>
