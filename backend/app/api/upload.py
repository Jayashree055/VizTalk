import pandas as pd
from fastapi import APIRouter, UploadFile, File
from app.database.connection import get_db_connection
from io import BytesIO

router = APIRouter()

@router.post("/upload")
async def upload_csv(file: UploadFile = File(...)):

    try:

        # Read file content
        contents = await file.read()

        # Try UTF-8 first
        try:
            df = pd.read_csv(
                BytesIO(contents),
                encoding="utf-8",
                on_bad_lines="skip"
            )

        except UnicodeDecodeError:

            df = pd.read_csv(
                BytesIO(contents),
                encoding="latin-1",
                on_bad_lines="skip"
            )

        # Clean column names
        df.columns = [col.strip().replace(" ", "_") for col in df.columns]

        conn = get_db_connection()

        df.to_sql("uploaded_data", conn, if_exists="replace", index=False)

        conn.close()

        return {
            "message": "File uploaded successfully",
            "columns": list(df.columns),
            "rows": len(df)
        }

    except Exception as e:

        return {
            "error": str(e)
        }