from app.services.llm_service import generate_sql

query = generate_sql("Show revenue by campaign type")

print("Generated SQL:")
print(query)