import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

st.set_page_config(page_title="Lifestyle & Disease Dashboard", layout="wide")

# -----------------------------------------------------------------------------
# Paths
# -----------------------------------------------------------------------------
DATA_PATH = Path(__file__).parent.parent / "data" / "brfss2022_enriched.csv"
COEF_PATH = Path(__file__).parent.parent / "data" / "diabetes_logit_coeffs.csv"

# -----------------------------------------------------------------------------
# Helper loaders (cached)
# -----------------------------------------------------------------------------
@st.cache_data(show_spinner=True)
def load_data():
    df = pd.read_csv(DATA_PATH)
    # Decode exercise to Yes/No for readability
    df["Exercise_Last30Days"] = df["Exercise_Last30Days"].replace({1: "Yes", 2: "No", "1": "Yes", "2": "No"})
    # Ensure ordered BMI classes
    bcat = pd.CategoricalDtype(
        ["Underweight", "Healthy", "Overweight", "Obese"], ordered=True
    )
    df["BMI_Class"] = df["BMI_Class"].astype(bcat)
    return df

@st.cache_data(show_spinner=True)
def load_coefficients():
    coef_df = pd.read_csv(COEF_PATH, index_col=0)
    return coef_df["coef"].to_dict()

df = load_data()
coeffs = load_coefficients()

# -----------------------------------------------------------------------------
# Age‑bucket ↔ code map (robust)
# -----------------------------------------------------------------------------
age_bucket_to_code = (
    df.groupby("Age_Bucket")["Age_Group"].agg(lambda x: x.mode().iloc[0]).to_dict()
)

# -----------------------------------------------------------------------------
# SIDEBAR FILTERS
# -----------------------------------------------------------------------------
st.sidebar.header("Filters")

age_options = list(age_bucket_to_code.keys())
selected_age = st.sidebar.multiselect("Age bucket", age_options, default=age_options)

gender_options = sorted(df["Sex"].dropna().unique())
selected_gender = st.sidebar.multiselect("Sex", gender_options, default=gender_options)

exercise_options = ["Yes", "No"]
selected_exer = st.sidebar.multiselect("Exercised in last 30 days", exercise_options, default=exercise_options)

bmi_options = ["Underweight", "Healthy", "Overweight", "Obese"]
selected_bmi = st.sidebar.multiselect("BMI class", bmi_options, default=bmi_options)

filtered_df = df[
    df["Age_Bucket"].isin(selected_age)
    & df["Sex"].isin(selected_gender)
    & df["Exercise_Last30Days"].isin(selected_exer)
    & df["BMI_Class"].isin(selected_bmi)
].copy()

st.sidebar.markdown(f"**Samples:** {len(filtered_df):,}")

# -----------------------------------------------------------------------------
# TAB SETUP
# -----------------------------------------------------------------------------
oview, heatmap_tab, predict_tab, cluster_tab, data_tab = st.tabs(
    ["Overview", "Risk Heat‑Map", "Risk Predictor", "Cluster Explorer", "Data"]
)

# -----------------------------------------------------------------------------
# 1 – OVERVIEW
# -----------------------------------------------------------------------------
with oview:
    st.subheader("Key Metrics (current filter)")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Sample Size", f"{len(filtered_df):,}")
    with col2:
        diabet_rate = (filtered_df["Diabetes"] == 1).mean()
        st.metric("Diabetes Prevalence", f"{diabet_rate:.1%}")
    with col3:
        heart_rate = (filtered_df["Heart_Disease"] == 1).mean()
        st.metric("Heart‑Disease Prevalence", f"{heart_rate:.1%}")

    fig, ax = plt.subplots(1, 2, figsize=(10, 4))
    sns.barplot(
        x="Exercise_Last30Days",
        y=(filtered_df["Diabetes"] == 1),
        estimator=np.mean,
        data=filtered_df,
        ax=ax[0],
    )
    ax[0].set_ylabel("Proportion with Diabetes")
    ax[0].set_title("Diabetes vs Exercise")

    sns.barplot(
        x="BMI_Class", y="BMI", data=filtered_df, ax=ax[1]
    )
    ax[1].set_ylabel("Mean BMI")
    ax[1].set_title("Average BMI by Class")

    plt.tight_layout()
    st.pyplot(fig)

# -----------------------------------------------------------------------------
# 2 – HEATMAP TAB
# -----------------------------------------------------------------------------
with heatmap_tab:
    st.subheader("Diabetes Prevalence by BMI Class & Exercise")
    piv = pd.pivot_table(
        filtered_df,
        values="Diabetes",
        index="BMI_Class",
        columns="Exercise_Last30Days",
        aggfunc=lambda x: (x == 1).mean(),
    ).reindex(index=bmi_options)

    fig_hm, ax_hm = plt.subplots(figsize=(3, 2))
    sns.heatmap(piv, annot=True, fmt=".1%", cmap="Reds", ax=ax_hm)
    st.pyplot(fig_hm)

# -----------------------------------------------------------------------------
# 3 – RISK PREDICTOR TAB
# -----------------------------------------------------------------------------
with predict_tab:
    st.subheader("Predict Your Diabetes Risk (Logit model)")
    colA, colB, colC, colD = st.columns([1, 1, 1, 2])

    with colA:
        bmi_in = st.number_input(
            "Body‑Mass Index", min_value=10.0, max_value=60.0, value=25.0, step=0.1
        )
    with colB:
        exer_in = st.radio("Exercised in last 30 days?", exercise_options, index=0)
    with colC:
        age_in = st.selectbox("Age bucket", age_options, index=age_options.index("45–49") if "45–49" in age_options else 0)

    # Build logit input vector
    const = coeffs.get("const", 0)
    age_code = age_bucket_to_code.get(age_in, 0)

    x_vec = (
        const
        + coeffs.get("BMI", 0) * bmi_in
        + coeffs.get("Exercise_Last30Days", 0) * (1 if exer_in == "Yes" else 0)
        + coeffs.get("Age_Group", 0) * age_code
    )

    prob = 1 / (1 + np.exp(-x_vec))

    with colD:
        st.metric("Predicted Diabetes Risk", f"{prob:.1%}")
        st.caption("*Model trained on 2022 BRFSS sample.")

# -----------------------------------------------------------------------------
# 4 – CLUSTER EXPLORER TAB
# -----------------------------------------------------------------------------
with cluster_tab:
    st.subheader("PCA of Lifestyle Clusters")

    # Build PCA only once per filter (cache inside tab)
    pca_cols = ["BMI", "Exercise_Last30Days", "Physical_Health_DaysPoor"]
    pca_df = filtered_df[pca_cols].copy()
    pca_df["Exercise_Last30Days"] = pca_df["Exercise_Last30Days"].replace({"Yes": 1, "No": 0})

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(pca_df)
    pcs = PCA(n_components=2, random_state=42).fit_transform(X_scaled)

    filtered_df["PC1"], filtered_df["PC2"] = pcs[:, 0], pcs[:, 1]

    colx, coly = st.columns(2)
    with colx:
        x_var = st.selectbox("X‑axis", ["PC1", "BMI", "Physical_Health_DaysPoor"], index=0)
    with coly:
        y_var = st.selectbox("Y‑axis", ["PC2", "BMI", "Physical_Health_DaysPoor"], index=1)

    fig_sc, ax_sc = plt.subplots(figsize=(6, 5))
    sns.scatterplot(
        x=x_var,
        y=y_var,
        hue="Cluster",
        palette="Set2",
        data=filtered_df,
        alpha=0.6,
        ax=ax_sc,
    )
    ax_sc.set_xlabel(x_var)
    ax_sc.set_ylabel(y_var)
    st.pyplot(fig_sc)

# -----------------------------------------------------------------------------
# 5 – DATA TAB
# -----------------------------------------------------------------------------
with data_tab:
    st.subheader("Filtered Data Table")
    st.dataframe(filtered_df.head(1000))
    st.download_button(
        label="Download current filter as CSV",
        data=filtered_df.to_csv(index=False).encode(),
        file_name="brfss_filtered.csv",
        mime="text/csv",
    )

st.caption("\u24D8 2022 CDC BRFSS – dashboard built with Streamlit")