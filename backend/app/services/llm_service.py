import os
import json
import requests
from dotenv import load_dotenv
import sqlite3

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")


def get_uploaded_schema():

    try:
        conn = sqlite3.connect("marketing.db")
        cursor = conn.cursor()

        cursor.execute("PRAGMA table_info(uploaded_data)")
        columns = cursor.fetchall()

        conn.close()

        if len(columns) == 0:
            return ""

        column_names = [col[1] for col in columns]

        return f"""
Table: uploaded_data
Columns:
{chr(10).join(column_names)}
"""

    except Exception:
        return ""


def generate_sql(user_prompt):

    base_schema = """
Table: campaigns

Columns:
Campaign_ID
Campaign_Type
Target_Audience
Duration
Channel_Used
Impressions
Clicks
Leads
Conversions
Revenue
Acquisition_Cost
ROI
Language
Engagement_Score
Customer_Segment
Date
"""

    uploaded_schema = get_uploaded_schema()

    schema = base_schema + "\n" + uploaded_schema

    prompt = f"""
You are a data analyst.

Convert the user's request into:

1. SQL query
2. Best chart type
3. X axis column
4. Y axis column

Database schema:
{schema}

Rules:

Use SQLite syntax
Do NOT explain anything
Return ONLY JSON
Prefer using uploaded_data if user asks about uploaded dataset
Aggregated columns must have aliases

Return JSON in this format:

{{
"sql": "SQL QUERY",
"chart": "bar | line | pie",
"x_axis": "column",
"y_axis": "column"
}}

User request:
{user_prompt}
"""

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "HTTP-Referer": "http://localhost:5173",
            "X-Title": "Conversational BI Dashboard"
        },
        json={
            "model": "deepseek/deepseek-chat",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
    )

    result = response.json()

    if "choices" not in result:
        raise Exception(f"OpenRouter API error: {result}")

    content = result["choices"][0]["message"]["content"]

    content = content.replace("```json", "").replace("```", "").strip()

    return json.loads(content)