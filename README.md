# DBX Retention Studio

**DBX Retention Studio** is an interactive Streamlit application built for the Databricks DNB Hackathon. It provides a visual and conversational interface for analyzing customer churn using Databricks SQL, dashboards, and Genie integration.

---

## Features

- **Interactive KPIs**: Displays total users, predicted churners, and churn rate.
- **Dynamic Filters**: Filter insights by country using the sidebar.
- **Custom Dashboards**:
  - Line chart: Predicted churners by customer tenure.
  - Pie chart: Churn distribution by platform.
  - Bar chart: Churn count by acquisition channel.
- **Genie Integration**: Launch a Databricks Genie room directly from the app to ask natural language questions.
- **Churn Segment Viewer**: Explore high-risk churn users in a structured table.
- **Real-time SQL Connectivity**: Powered by `databricks-sql-connector` with secure `.env` configuration.

---

## Screenshots

![Dashboard Screenshot](path/to/your/screenshot.png) <!-- Replace with actual screenshot path -->

---

## Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/your-username/dbx-retention-studio.git
cd dbx-retention-studio
```

### 2. Create `.env` File

Create a `.env` file in the root directory and add your Databricks credentials:

```dotenv
DATABRICKS_HOSTNAME=your-hostname
DATABRICKS_HTTP_PATH=your-http-path
DATABRICKS_TOKEN=your-personal-access-token
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the App

```bash
streamlit run app.py
```

---

## Tech Stack

- [Databricks SQL](https://www.databricks.com/product/databricks-sql)
- [Streamlit](https://streamlit.io/)
- [Plotly](https://plotly.com/python/)
- [Genie](https://docs.databricks.com/en/genie/index.html) (Databricks chatbot)
- Python, Pandas, SQL

---

## Genie Room

You can access the Genie room via the app or directly here:  
[Launch Genie](https://dbc-12a1b15e-49dd.cloud.databricks.com/genie/rooms/01f05d11ddb11e70b1463cc6262bd385?o=240024990044367)

---

## Acknowledgements

Thanks to the Databricks team for organizing the DNB Hackathon and providing an amazing opportunity to learn and build with the platform.

---

## Contact

Note: The hackathon contact email (`dnb-hackathon@databricks.com`) currently returns a bounce error stating that the group may not exist or accept external emails.

---

## License

This project is intended for educational/demo purposes and may include proprietary dashboard links tied to a Databricks workspace.
