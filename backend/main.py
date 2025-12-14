import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.core.logging import setup_logging
from backend.core.middleware import RequestLoggingMiddleware, RateLimitMiddleware
from backend.core.error_handling import install_exception_handlers
from backend.api.alpha_routes import router as alpha_router
from backend.api.calc_routes import router as calc_router


setup_logging()
logger = logging.getLogger("app.main")

app = FastAPI(title="Binance Alpha Tool API")

# Middlewares
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(RateLimitMiddleware)

# CORS (adjust as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handling
install_exception_handlers(app)

# Routers
app.include_router(alpha_router)
app.include_router(calc_router)


@app.get("/health")
async def health():
    return {"status": "ok"}
