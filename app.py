import streamlit as st
from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd
import os

# Initialize BigQuery client
def initialize_bigquery_client(json_key_path):
    try:
        # client = bigquery.Client.from_service_account_json('cb-comp-eng.json')
        # return client
        # api_json=os.getenv('SA')
        api_json=os.getenv('SA_Royal')
        credentials = service_account.Credentials.from_service_account_info(eval(api_json))
        client = bigquery.Client(credentials=credentials, project=credentials.project_id)
        return client
    except Exception as e:
        st.error(f"Failed to authenticate with the provided JSON: {e}")
        return None
    

# Query BigQuery table
def query_bigquery_table(client, table_name):
    query = f"SELECT * FROM `{table_name}` LIMIT 100"  # Adjust LIMIT as needed
    try:
        query_job = client.query(query)
        results = query_job.result()
        df = results.to_dataframe()
        return df
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

# Streamlit app
def main():
    st.title("BigQuery Table Viewer")
    st.write("Enter the table name below to fetch data from BigQuery.")

    # Path to JSON key file
    json_key_path = st.text_input("Enter the path to your Google Cloud JSON key file:", type="password")

    # Input for table name
    table_name = st.text_input("Enter the BigQuery table name (format: `project.dataset.table`):")

    # Button to run query
    if st.button("Run Query"):
        if json_key_path and table_name:
            with st.spinner("Querying BigQuery..."):
                client = initialize_bigquery_client(json_key_path)
                df = query_bigquery_table(client, table_name)
                if df is not None:
                    st.success("Query executed successfully!")
                    st.write("Here are the results:")
                    st.dataframe(df)
                else:
                    st.error("No data found or an error occurred.")
        else:
            st.warning("Please provide both the JSON key file path and the table name.")

if __name__ == "__main__":
    main()
