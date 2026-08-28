import streamlit as st
import pandas as pd
import plotly.express as px

from database import initialize_database, seed_data, get_records_dataframe


st.set_page_config(
    page_title="Financial Inclusion Analytics",
    page_icon="🏦",
    layout="wide"
)


initialize_database()
seed_data()


df = get_records_dataframe()


st.title("🏦 Financial Inclusion & Microfinance Access Analytics Dashboard")
st.caption("Financial access, savings, lending and household vulnerability analysis")


st.sidebar.header("Filters")


districts = sorted(df["district"].unique())

selected_districts = st.sidebar.multiselect(
    "District",
    districts,
    default=districts
)


genders = sorted(df["gender"].unique())

selected_genders = st.sidebar.multiselect(
    "Gender",
    genders,
    default=genders
)


levels = sorted(df["vulnerability_level"].unique())

selected_levels = st.sidebar.multiselect(
    "Vulnerability Level",
    levels,
    default=levels
)


filtered_df = df[
    df["district"].isin(selected_districts)
    & df["gender"].isin(selected_genders)
    & df["vulnerability_level"].isin(selected_levels)
].copy()


if filtered_df.empty:
    st.warning("No records match the selected filters.")
    st.stop()


st.header("Executive Overview")


households = len(filtered_df)

bank_access = filtered_df["bank_account"].mean() * 100

mobile_access = filtered_df["mobile_finance"].mean() * 100

loan_access = filtered_df["loan_access"].mean() * 100

formal_access = filtered_df["formal_finance"].mean() * 100

avg_savings = filtered_df["savings_amount"].mean()

avg_vulnerability = filtered_df["financial_vulnerability"].mean()


c1, c2, c3, c4, c5, c6 = st.columns(6)


c1.metric("Households", f"{households:,}")

c2.metric("Bank Access", f"{bank_access:.1f}%")

c3.metric("Mobile Finance", f"{mobile_access:.1f}%")

c4.metric("Loan Access", f"{loan_access:.1f}%")

c5.metric("Formal Finance", f"{formal_access:.1f}%")

c6.metric("Avg. Savings", f"{avg_savings:,.0f}")


st.divider()


st.header("Financial Service Access")


access_data = pd.DataFrame({
    "Indicator": [
        "Bank Account",
        "Mobile Finance",
        "Formal Finance",
        "Insurance"
    ],
    "Access Rate": [
        filtered_df["bank_account"].mean() * 100,
        filtered_df["mobile_finance"].mean() * 100,
        filtered_df["formal_finance"].mean() * 100,
        filtered_df["insurance_access"].mean() * 100
    ]
})


fig = px.bar(
    access_data,
    x="Indicator",
    y="Access Rate",
    text="Access Rate",
    title="Financial Service Access Rate"
)


fig.update_traces(
    texttemplate="%{text:.1f}%",
    textposition="outside"
)


fig.update_layout(
    yaxis_title="Access (%)",
    xaxis_title=""
)


st.plotly_chart(fig, use_container_width=True)


st.header("District-wise Financial Inclusion")


district_data = (
    filtered_df
    .groupby("district", as_index=False)
    .agg(
        Bank_Access=("bank_account", "mean"),
        Mobile_Finance=("mobile_finance", "mean"),
        Formal_Finance=("formal_finance", "mean"),
        Loan_Access=("loan_access", "mean")
    )
)


district_long = district_data.melt(
    id_vars="district",
    var_name="Indicator",
    value_name="Rate"
)


district_long["Rate"] = district_long["Rate"] * 100


fig = px.bar(
    district_long,
    x="district",
    y="Rate",
    color="Indicator",
    barmode="group",
    title="Financial Access by District"
)


fig.update_layout(
    yaxis_title="Access Rate (%)",
    xaxis_title="District"
)


st.plotly_chart(fig, use_container_width=True)


st.header("Savings Analysis")


savings_data = (
    filtered_df
    .groupby("district", as_index=False)["savings_amount"]
    .mean()
    .sort_values("savings_amount", ascending=False)
)


fig = px.bar(
    savings_data,
    x="district",
    y="savings_amount",
    text="savings_amount",
    title="Average Savings by District"
)


fig.update_traces(
    texttemplate="%{text:.0f}",
    textposition="outside"
)


fig.update_layout(
    yaxis_title="Average Savings",
    xaxis_title="District"
)


st.plotly_chart(fig, use_container_width=True)


st.header("Loan Analysis")


loan_df = filtered_df[
    filtered_df["loan_access"] == 1
].copy()


if not loan_df.empty:

    col1, col2 = st.columns(2)


    with col1:

        loan_source = (
            loan_df
            .groupby("loan_source", as_index=False)
            .agg(
                Average_Loan=("loan_amount", "mean")
            )
        )


        fig = px.bar(
            loan_source,
            x="loan_source",
            y="Average_Loan",
            text="Average_Loan",
            title="Average Loan Amount by Source"
        )


        fig.update_traces(
            texttemplate="%{text:.0f}",
            textposition="outside"
        )


        fig.update_layout(
            yaxis_title="Average Loan Amount",
            xaxis_title="Loan Source"
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


    with col2:

        purpose = (
            loan_df["loan_purpose"]
            .value_counts()
            .reset_index()
        )


        purpose.columns = [
            "Loan Purpose",
            "Households"
        ]


        fig = px.pie(
            purpose,
            names="Loan Purpose",
            values="Households",
            title="Loan Purpose Distribution"
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )

else:

    st.info("No loan records available.")


st.header("Financial Vulnerability")


col1, col2 = st.columns(2)


with col1:

    vulnerability = (
        filtered_df["vulnerability_level"]
        .value_counts()
        .reset_index()
    )


    vulnerability.columns = [
        "Vulnerability Level",
        "Households"
    ]


    fig = px.pie(
        vulnerability,
        names="Vulnerability Level",
        values="Households",
        hole=0.4,
        title="Vulnerability Distribution"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


with col2:

    vulnerability_district = (
        filtered_df
        .groupby("district", as_index=False)
        ["financial_vulnerability"]
        .mean()
        .sort_values(
            "financial_vulnerability",
            ascending=False
        )
    )


    fig = px.bar(
        vulnerability_district,
        x="district",
        y="financial_vulnerability",
        text="financial_vulnerability",
        title="Average Vulnerability by District"
    )


    fig.update_traces(
        texttemplate="%{text:.1f}",
        textposition="outside"
    )


    fig.update_layout(
        yaxis_title="Vulnerability Score",
        xaxis_title="District"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


st.header("Financial Literacy & Loan Repayment")


col1, col2 = st.columns(2)


with col1:

    literacy = (
        filtered_df
        .groupby("district", as_index=False)
        ["financial_literacy"]
        .mean()
        .sort_values(
            "financial_literacy",
            ascending=False
        )
    )


    fig = px.bar(
        literacy,
        x="district",
        y="financial_literacy",
        text="financial_literacy",
        title="Financial Literacy by District"
    )


    fig.update_traces(
        texttemplate="%{text:.1f}",
        textposition="outside"
    )


    fig.update_layout(
        yaxis_title="Literacy Score",
        xaxis_title="District"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


with col2:

    if not loan_df.empty:

        repayment = (
            loan_df
            .groupby("loan_source", as_index=False)
            ["repayment_rate"]
            .mean()
        )


        fig = px.bar(
            repayment,
            x="loan_source",
            y="repayment_rate",
            text="repayment_rate",
            title="Loan Repayment Rate"
        )


        fig.update_traces(
            texttemplate="%{text:.1f}%",
            textposition="outside"
        )


        fig.update_layout(
            yaxis_title="Repayment Rate (%)",
            xaxis_title="Loan Source"
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.info("No repayment records available.")


st.header("Household Records")


table_columns = [
    "district",
    "upazila",
    "gender",
    "age_group",
    "monthly_income",
    "bank_account",
    "mobile_finance",
    "savings_amount",
    "loan_access",
    "loan_amount",
    "financial_literacy",
    "financial_vulnerability",
    "vulnerability_level"
]


table_df = filtered_df[table_columns].copy()


table_df = table_df.rename(
    columns={
        "district": "District",
        "upazila": "Upazila",
        "gender": "Gender",
        "age_group": "Age Group",
        "monthly_income": "Monthly Income",
        "bank_account": "Bank Account",
        "mobile_finance": "Mobile Finance",
        "savings_amount": "Savings",
        "loan_access": "Loan Access",
        "loan_amount": "Loan Amount",
        "financial_literacy": "Financial Literacy",
        "financial_vulnerability": "Vulnerability Score",
        "vulnerability_level": "Vulnerability Level"
    }
)


st.dataframe(
    table_df,
    use_container_width=True,
    hide_index=True
)


st.divider()


st.subheader("Key Insights")


highest_vulnerability_district = (
    filtered_df
    .groupby("district")["financial_vulnerability"]
    .mean()
    .idxmax()
)


st.info(
    f"Average financial vulnerability score: "
    f"**{avg_vulnerability:.1f}**"
)


st.info(
    f"Highest average vulnerability is observed in "
    f"**{highest_vulnerability_district}**."
)


st.caption(
    "Financial Inclusion & Microfinance Access Analytics | "
    "Python • SQLite • Pandas • Plotly • Streamlit"
)
