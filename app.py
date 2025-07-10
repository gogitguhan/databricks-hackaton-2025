import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import databricks.sql
import os
from dotenv import load_dotenv

# -------------------------
# Load environment variables from .env file
# -------------------------
load_dotenv()

# -------------------------
# Databricks SQL Connection
# -------------------------
connection = databricks.sql.connect(
    server_hostname=os.getenv("DATABRICKS_HOSTNAME"),
    http_path=os.getenv("DATABRICKS_HTTP_PATH"),
    access_token=os.getenv("DATABRICKS_TOKEN")
)

def query_to_df(sql):
    with connection.cursor() as cursor:
        cursor.execute(sql)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
    return pd.DataFrame(rows, columns=columns)

# -------------------------
# UI Setup
# -------------------------
st.set_page_config(page_title="DBX Retention Studio", layout="wide")
st.title("📉 DBX Retention Studio")
st.caption("App to manage customer churn trends and engage with Genie — powered by Databricks.")

# -------------------------
# Country Filter
# -------------------------
st.sidebar.header("🔍 Filter")
country_filter = st.sidebar.selectbox("Select Country", ["All", "USA", "FR", "SPAIN"])

# -------------------------
# KPI Section
# -------------------------
st.subheader("⚙️ Key Churn Metrics")
query_kpis = f"""
SELECT COUNT(*) AS total_users,
       SUM(CASE WHEN churn_prediction = 1 THEN 1 ELSE 0 END) AS predicted_churners
FROM data_pioneers.c360.churn_prediction
{f"WHERE country = '{country_filter}'" if country_filter != "All" else ""}
"""
df_kpis = query_to_df(query_kpis)
total_users = int(df_kpis['total_users'][0])
predicted_churners = int(df_kpis['predicted_churners'][0])
churn_rate = round((predicted_churners / total_users) * 100, 2) if total_users else 0

col1, col2, col3 = st.columns(3)
col1.metric("Total Users", total_users)
col2.metric("Predicted Churners", predicted_churners)
col3.metric("Churn Rate", f"{churn_rate}%", delta=f"{churn_rate - 15:.1f}%")

# -------------------------
# 📈 Rebuilt Dashboard Chart (Churn by Tenure)
# -------------------------
st.subheader("📊 Predicted Churn by Tenure")
tenure_query = f"""
SELECT CAST(days_since_creation / 30 AS INT) AS tenure_months,
       COUNT(*) AS user_count
FROM data_pioneers.c360.churn_prediction
WHERE churn_prediction = 1
{f"AND country = '{country_filter}'" if country_filter != "All" else ""}
GROUP BY tenure_months
ORDER BY tenure_months
"""
df_tenure = query_to_df(tenure_query)
fig = px.line(df_tenure, x="tenure_months", y="user_count", markers=True,
              labels={"tenure_months": "Customer Tenure (Months)", "user_count": "Predicted Churners"},
              title="Predicted Churners by Customer Tenure")
st.plotly_chart(fig, use_container_width=True)

# -------------------------
# 🥧 New Chart: Churn Distribution by Platform (Pie Chart)
# -------------------------
st.subheader("🥧 Churn Distribution by Platform")
pie_query = f"""
SELECT platform, COUNT(*) AS churned_users
FROM data_pioneers.c360.churn_prediction
WHERE churn_prediction = 1
{f"AND country = '{country_filter}'" if country_filter != "All" else ""}
GROUP BY platform
"""
df_pie = query_to_df(pie_query)
fig_pie = px.pie(df_pie, values="churned_users", names="platform", title="Predicted Churn by Platform",
                 color_discrete_sequence=px.colors.sequential.RdBu)
st.plotly_chart(fig_pie, use_container_width=True)

# -------------------------
# 📊 New Chart: Churn by Channel (Bar Chart)
# -------------------------
st.subheader("📊 Churn Count by Acquisition Channel")
bar_query = f"""
SELECT canal AS channel, COUNT(*) AS churned_users
FROM data_pioneers.c360.churn_prediction
WHERE churn_prediction = 1
{f"AND country = '{country_filter}'" if country_filter != "All" else ""}
GROUP BY canal
ORDER BY churned_users DESC
"""
df_bar = query_to_df(bar_query)
fig_bar = px.bar(df_bar, x="channel", y="churned_users",
                 labels={"channel": "Acquisition Channel", "churned_users": "Churned Users"},
                 title="Churned Users by Acquisition Channel",
                 color="churned_users", color_continuous_scale="Viridis")
st.plotly_chart(fig_bar, use_container_width=True)

# -------------------------
# 📁 Segment Preview
# -------------------------
with st.expander("📁 View Predicted Churners"):
    segment_query = f"""
    SELECT user_id, country, canal, platform, churn_prediction, session_count, total_amount
    FROM data_pioneers.c360.churn_prediction
    WHERE churn_prediction = 1
    {f"AND country = '{country_filter}'" if country_filter != "All" else ""}
    LIMIT 50
    """
    df_segment = query_to_df(segment_query)
    st.dataframe(df_segment)
    

# -------------------------
# 💬 Genie Launch Link
# -------------------------
st.subheader("💬 Ask Genie")
st.markdown(
    "[🪄 Launch Genie in a new tab](https://dbc-12a1b15e-49dd.cloud.databricks.com/genie/rooms/01f05d11ddb11e70b1463cc6262bd385?o=240024990044367)",
    unsafe_allow_html=True
)

# -------------------------
# Footer
# -------------------------
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
