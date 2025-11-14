from fastapi import FastAPI

from app.api.cotacao_rotas import router as cotacao_router

app = FastAPI(
    title="Serviço de Cotação de Moedas",
    description="Serviço simples com cache em memória para cotação de moedas.",
    version="0.1.0",
)

app.include_router(cotacao_router)


@app.get("/health")
async def healthcheck():
    return {"status": "ok"}
