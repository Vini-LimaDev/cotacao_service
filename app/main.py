# app/main.py
from fastapi import FastAPI

from app.api.cotacao_rotas import router as cotacao_router

app = FastAPI(
    title="Serviço de Cotação de Moedas",
    description="Serviço com cache em memória usando Frankfurter API.",
    version="0.2.0",
)

app.include_router(cotacao_router)


@app.get("/health")
async def healthcheck():
    return {"status": "ok"}
