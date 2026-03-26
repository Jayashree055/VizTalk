from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from app.api.upload import router as upload_router
from app.services.query_service import run_natural_language_query
from app.database.db_setup import load_csv_to_db

app = FastAPI()
@app.on_event("startup")
def startup_event():
    load_csv_to_db()
# register router
app.include_router(upload_router)

# Allow frontend access
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    prompt: str


@app.get("/")
def home():
    return {"message": "Conversational BI API running"}


@app.post("/query")
def query_data(request: QueryRequest):
    result = run_natural_language_query(request.prompt)
    return result