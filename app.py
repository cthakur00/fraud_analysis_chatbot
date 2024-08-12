import streamlit as st
import pandas as pd
import sqlite3
from sqlalchemy import create_engine, text
import openai
import config
from langchain.llms import OpenAI as LangChainOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# Initialize the OpenAI client with your API key
openai.api_key = config.api_key

# Streamlit app layout
st.title("💳Credit Card Fraud Detection Chatbot")

# File upload
uploaded_file = st.file_uploader("Upload the Credit Card Fraud CSV file", type="csv")

if uploaded_file is not None:
    # Load the CSV file into a DataFrame
    df = pd.read_csv(uploaded_file)
    st.write("First few rows of the dataset:")
    st.write(df.head())

    # Create an SQLite database
    engine = create_engine('sqlite:///fraud_detection.db')
    df.to_sql('fraud_data', con=engine, if_exists='replace', index=False)

    
    st.success("Data loaded into the SQLite database successfully!")

    # Query input
    query_input = st.text_input("Ask a question related to the data:")

    if query_input:
        # Set up LangChain to use OpenAI
        llm = LangChainOpenAI(
            openai_api_key=config.api_key,
            temperature=0.2
        )
        
        # Define a prompt template
        prompt = PromptTemplate(
            input_variables=["question"],
            template="Translate this natural language question into a SQL query: {question}"
        )

        # Create an LLM chain with the prompt and the LLM
        chain = LLMChain(llm=llm, prompt=prompt)

        # Generate SQL query using the LLM chain
        sql_query = chain.run(query_input)
        st.write(f"Generated SQL Query: {sql_query}")

        # Execute the generated SQL query and display results
        try:
            conn = engine.connect()
            result = conn.execute(text(sql_query))
            st.write("Query Result:")
            st.write(result.fetchall())
        except Exception as e:
            st.error(f"Error executing SQL query: {e}")


#sample questions:
#how many category are there in the fraud_data?
#What is the total amt  grouped by state in the fraud_data ?
#How many fraudulent transactions (isfraud = 1) are there in each city in the fraud_data dataset?
#How many transactions occurred in the fraud_data where the category is 'health_fitness' and the amt is greater than 100?
