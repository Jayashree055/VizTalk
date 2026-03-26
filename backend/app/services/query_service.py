import pandas as pd
import numpy as np
from app.database.connection import get_db_connection
from app.services.llm_service import generate_sql


def run_natural_language_query(user_prompt, context=None):

    # Combine previous query context if available
    if context:
        combined_prompt = context + "\nUser follow-up: " + user_prompt
    else:
        combined_prompt = user_prompt

    # Generate SQL using LLM
    llm_result = generate_sql(combined_prompt)

    sql_query = llm_result["sql"]
    chart_type = llm_result["chart"]
    x_axis = llm_result["x_axis"]
    y_axis = llm_result["y_axis"]

    conn = get_db_connection()

    df = pd.read_sql(sql_query, conn)

    conn.close()

    # Replace NaN / inf values
    df = df.replace([np.nan, np.inf, -np.inf], None)

    return {
        "sql": sql_query,
        "chart": chart_type,
        "x": x_axis,
        "y": y_axis,
        "data": df.to_dict(orient="records")
    }