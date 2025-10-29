from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models.ehr_event import EHREvent # pyright: ignore[reportMissingImports]
from app.services.ehr_validator import load_dfa, validate_sequence

app = FastAPI(title="EHR Finite Automata Validator")

# ✅ Allow your React frontend to connect
origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:3001"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,   # allow requests from frontend
    allow_credentials=True,
    allow_methods=["*"],     # allow all methods (GET, POST, etc.)
    allow_headers=["*"],     # allow all headers
)

dfa = load_dfa()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/validate")
def validate_ehr(events: list[EHREvent]):
    result = validate_sequence(events, dfa)
    return result
