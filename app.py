import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt

# -----------------------------
# Load Models & Data
# -----------------------------

risk_model = joblib.load("models/risk_model.pkl")
loan_model = joblib.load("models/loan_model.pkl")

df = pd.read_csv("dataset/german_credit_data.csv")

# -----------------------------
# Page Config
# -----------------------------

st.set_page_config(
    page_title="Banking Risk Analysis System",
    layout="wide"
)

st.title("🏦 Banking Risk Analysis System")
st.markdown(
    "Predict customer credit risk and estimate recommended loan amount."
)

# -----------------------------
# Mappings
# -----------------------------

CHECKING_ACCOUNT = {
    "No Checking Account": 1,
    "< 0 DM": 2,
    "0 - 200 DM": 3,
    "≥ 200 DM / Salary ≥ 1 Year": 4
}

CREDIT_HISTORY = {
    "Delay In Past Payments": 0,
    "Critical Account / Other Credits": 1,
    "All Credits Paid": 2,
    "Existing Credits Paid Duly": 3,
    "All Credits At This Bank Paid": 4
}

PURPOSE = {
    "Others": 0,
    "New Car": 1,
    "Used Car": 2,
    "Furniture / Equipment": 3,
    "Radio / Television": 4,
    "Domestic Appliances": 5,
    "Repairs": 6,
    "Vacation": 8,
    "Retraining": 9,
    "Business": 10
}

SAVINGS = {
    "Unknown / No Savings": 1,
    "< 100 DM": 2,
    "100 - 500 DM": 3,
    "500 - 1000 DM": 4,
    "≥ 1000 DM": 5
}

EMPLOYMENT = {
    "Unemployed": 1,
    "< 1 Year": 2,
    "1 - 4 Years": 3,
    "4 - 7 Years": 4,
    "≥ 7 Years": 5
}

PERSONAL_STATUS = {
    "Male Divorced / Separated": 1,
    "Female Non-Single / Male Single": 2,
    "Male Married / Widowed": 3,
    "Female Single": 4
}

PROPERTY = {
    "No Property": 1,
    "Car / Other Property": 2,
    "Life Insurance": 3,
    "Real Estate": 4
}

OTHER_INSTALLMENT = {
    "Bank": 1,
    "Stores": 2,
    "None": 3
}

HOUSING = {
    "Free": 1,
    "Rent": 2,
    "Own": 3
}

JOB = {
    "Unemployed / Unskilled Non Resident": 1,
    "Unskilled Resident": 2,
    "Skilled Employee": 3,
    "Manager / Self Employed": 4
}

TELEPHONE = {
    "No": 1,
    "Yes": 2
}

FOREIGN_WORKER = {
    "Yes": 1,
    "No": 2
}

# -----------------------------
# Sidebar Form
# -----------------------------

st.sidebar.header("Customer Details")

data = {}

data["alter"] = st.sidebar.number_input(
    "Age",
    min_value=18,
    max_value=100,
    value=30
)

data["laufzeit"] = st.sidebar.number_input(
    "Loan Duration (Months)",
    min_value=1,
    max_value=120,
    value=24
)

checking = st.sidebar.selectbox(
    "Checking Account Status",
    list(CHECKING_ACCOUNT.keys())
)
data["laufkont"] = CHECKING_ACCOUNT[checking]

history = st.sidebar.selectbox(
    "Credit History",
    list(CREDIT_HISTORY.keys())
)
data["moral"] = CREDIT_HISTORY[history]

purpose = st.sidebar.selectbox(
    "Loan Purpose",
    list(PURPOSE.keys())
)
data["verw"] = PURPOSE[purpose]

savings = st.sidebar.selectbox(
    "Savings Account Status",
    list(SAVINGS.keys())
)
data["sparkont"] = SAVINGS[savings]

employment = st.sidebar.selectbox(
    "Employment Duration",
    list(EMPLOYMENT.keys())
)
data["beszeit"] = EMPLOYMENT[employment]

data["rate"] = st.sidebar.selectbox(
    "Installment Rate",
    [1, 2, 3, 4]
)

personal = st.sidebar.selectbox(
    "Personal Status",
    list(PERSONAL_STATUS.keys())
)
data["famges"] = PERSONAL_STATUS[personal]

data["buerge"] = st.sidebar.selectbox(
    "Other Debtors / Guarantors",
    [1, 2, 3]
)

data["wohnzeit"] = st.sidebar.selectbox(
    "Years At Current Residence",
    [1, 2, 3, 4]
)

property_type = st.sidebar.selectbox(
    "Property Type",
    list(PROPERTY.keys())
)
data["verm"] = PROPERTY[property_type]

other_plan = st.sidebar.selectbox(
    "Other Installment Plans",
    list(OTHER_INSTALLMENT.keys())
)
data["weitkred"] = OTHER_INSTALLMENT[other_plan]

housing = st.sidebar.selectbox(
    "Housing Status",
    list(HOUSING.keys())
)
data["wohn"] = HOUSING[housing]

data["bishkred"] = st.sidebar.selectbox(
    "Number Of Existing Credits",
    [1, 2, 3, 4]
)

job = st.sidebar.selectbox(
    "Job Type",
    list(JOB.keys())
)
data["beruf"] = JOB[job]

data["pers"] = st.sidebar.selectbox(
    "People Liable",
    [1, 2]
)

telephone = st.sidebar.selectbox(
    "Telephone Available",
    list(TELEPHONE.keys())
)
data["telef"] = TELEPHONE[telephone]

worker = st.sidebar.selectbox(
    "Foreign Worker",
    list(FOREIGN_WORKER.keys())
)
data["gastarb"] = FOREIGN_WORKER[worker]

user_input = pd.DataFrame([data])
feature_cols = [
    'laufkont',
    'laufzeit',
    'moral',
    'verw',
    'sparkont',
    'beszeit',
    'rate',
    'famges',
    'buerge',
    'wohnzeit',
    'verm',
    'alter',
    'weitkred',
    'wohn',
    'bishkred',
    'beruf',
    'pers',
    'telef',
    'gastarb'
]

user_input = user_input[feature_cols]
# -----------------------------
# Tabs
# -----------------------------

tab1, tab2, tab3 = st.tabs(
    ["Credit Risk", "Loan Amount", "Analytics"]
)

# -----------------------------
# Credit Risk
# -----------------------------

with tab1:

    st.subheader("Credit Risk Prediction")

    if st.button("Predict Credit Risk"):

        prediction = risk_model.predict(user_input)[0]

        if prediction == 1:
            st.success("✅ Good Credit Risk")
        else:
            st.error("❌ Bad Credit Risk")

# -----------------------------
# Loan Amount
# -----------------------------

with tab2:

    st.subheader("Loan Amount Recommendation")

    if st.button("Predict Loan Amount"):

        amount = loan_model.predict(user_input)[0]

        st.success(
            f"💰 Recommended Loan Amount: {amount:,.0f} DM"
        )

# -----------------------------
# Analytics
# -----------------------------

with tab3:

    st.header("📊 Dataset Analytics")

    # -------------------------
    # Credit Risk Distribution
    # -------------------------

    st.subheader("Credit Risk Distribution")

    risk_df = df.copy()

    risk_df["kredit"] = risk_df["kredit"].map({
        0: "Bad",
        1: "Good"
    })

    fig, ax = plt.subplots()

    risk_df["kredit"].value_counts().plot(
        kind="bar",
        ax=ax
    )

    ax.set_xlabel("Credit Risk")
    ax.set_ylabel("Number of Customers")
    ax.set_title("Credit Risk Distribution")

    st.pyplot(fig)

    # -------------------------
    # Loan Amount Distribution
    # -------------------------

    st.subheader("Loan Amount Distribution")

    fig2, ax2 = plt.subplots()

    df["hoehe"].hist(
        bins=20,
        ax=ax2
    )

    ax2.set_xlabel("Loan Amount (DM)")
    ax2.set_ylabel("Frequency")
    ax2.set_title("Loan Amount Distribution")

    st.pyplot(fig2)

    # -------------------------
    # Human Readable Dataset
    # -------------------------

    st.subheader("Dataset Preview")

    display_df = df.copy()

    display_df.rename(
        columns={
            "laufkont": "Checking Account",
            "laufzeit": "Loan Duration",
            "moral": "Credit History",
            "verw": "Purpose",
            "hoehe": "Loan Amount",
            "sparkont": "Savings Account",
            "beszeit": "Employment Duration",
            "rate": "Installment Rate",
            "famges": "Personal Status",
            "buerge": "Other Debtors",
            "wohnzeit": "Residence Duration",
            "verm": "Property",
            "alter": "Age",
            "weitkred": "Other Installment Plans",
            "wohn": "Housing",
            "bishkred": "Existing Credits",
            "beruf": "Job",
            "pers": "People Liable",
            "telef": "Telephone",
            "gastarb": "Foreign Worker",
            "kredit": "Credit Risk"
        },
        inplace=True
    )

    # Convert codes to readable labels

    display_df["Credit Risk"] = display_df["Credit Risk"].map({
        0: "Bad",
        1: "Good"
    })

    display_df["Housing"] = display_df["Housing"].map({
        1: "Free",
        2: "Rent",
        3: "Own"
    })

    display_df["Foreign Worker"] = display_df["Foreign Worker"].map({
        1: "Yes",
        2: "No"
    })

    display_df["Telephone"] = display_df["Telephone"].map({
        1: "No",
        2: "Yes"
    })

    display_df["Job"] = display_df["Job"].map({
        1: "Unemployed/Unskilled Non-Resident",
        2: "Unskilled Resident",
        3: "Skilled Employee",
        4: "Manager/Self-Employed"
    })

    display_df["Other Installment Plans"] = display_df[
        "Other Installment Plans"
    ].map({
        1: "Bank",
        2: "Stores",
        3: "None"
    })

    display_df["Savings Account"] = display_df[
        "Savings Account"
    ].map({
        1: "No Savings",
        2: "<100 DM",
        3: "100-500 DM",
        4: "500-1000 DM",
        5: ">=1000 DM"
    })

    show_raw = st.checkbox(
        "Show Original German Dataset"
    )

    if show_raw:
        st.dataframe(
            df.head(20),
            use_container_width=True
        )
    else:
        st.dataframe(
            display_df.head(20),
            use_container_width=True
        )

    # -------------------------
    # Dataset Summary
    # -------------------------

    st.subheader("Dataset Summary")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Records",
            len(df)
        )

    with col2:
        st.metric(
            "Average Loan Amount",
            f"{df['hoehe'].mean():.0f} DM"
        )

    with col3:
        st.metric(
            "Average Age",
            f"{df['alter'].mean():.0f}"
        )