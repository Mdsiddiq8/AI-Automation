import os
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# STEP 1 & 2: Load and Read the CSV File
input_file_path = "data/students_raw.csv"

try:
    df_raw = pd.read_csv(input_file_path)
    print("--- RAW DATA PREVIEW ---")
    print(df_raw.head())
    print(f"\nTotal records loaded: {len(df_raw)}")
except FileNotFoundError:
    print(f"Error: The file '{input_file_path}' was not found. Please check the path.")

import json

def clean_data_with_openai(dataframe: pd.DataFrame) -> pd.DataFrame:
    # Convert raw dataframe to JSON string for the prompt
    raw_json_str = dataframe.to_json(orient="records")

    prompt = f"""
    You are a data cleaning engine. Fix all errors in the following student dataset.
    
    Cleaning Rules:
    1. Standardize student names (Proper Case).
    2. Standardize dates to YYYY-MM-DD format.
    3. Fix obvious typos in email addresses or department names.
    4. Fill missing values with appropriate defaults (e.g., "Unknown" or standard defaults).
    
    Return ONLY a JSON array of objects with the exact same key structure as the input.
    Do not include markdown headers or conversational text outside the JSON.

    Raw Data:
    {raw_json_str}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a precise data transformation API."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.0
    )

    cleaned_content = response.choices[0].message.content.strip()
    
    # Strip markdown formatting if returned by the API
    if cleaned_content.startswith("```json"):
        cleaned_content = cleaned_content.replace("```json", "").replace("```", "").strip()

    cleaned_data_list = json.loads(cleaned_content)
    return pd.DataFrame(cleaned_data_list)