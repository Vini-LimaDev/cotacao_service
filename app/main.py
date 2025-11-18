from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.cotacao_rotas import router as cotacao_router
from app.api.auth_rotas import router as auth_router
from app.api.cripto_rotas import router as cripto_router

# Inicializa a aplicação FastAPI
app = FastAPI(
    title="Serviço de Cotação de Moedas",
    description="Serviço com autenticação JWT e cache em memória usando Frankfurter API.",
    version="0.3.0",
)

# 🔹 CORS: libera o front do Vite (porta 5173)
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui as rotas de autenticação
app.include_router(auth_router)

# Inclui as rotas de cotação
app.include_router(cotacao_router)

# Inclui as rotas de criptomoedas
app.include_router(cripto_router)


@app.get("/health")
# Endpoint para verificar a saúde da aplicação
async def healthcheck():
    return {"status": "ok"}
