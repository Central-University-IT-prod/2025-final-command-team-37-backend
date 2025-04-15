import contextlib

import sentry_sdk
import uvicorn
from asgi_monitor.integrations.fastapi import MetricsConfig, setup_metrics
from dishka.integrations.fastapi import setup_dishka
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from api.v1 import root_router
from core.build import create_async_container
from core.config import Config, create_config
from core.exceptions import setup_exception_handlers
from infrastructure.ioc.registry import get_providers


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await app.state.dishka_container.close()


def create_app() -> FastAPI:
    metrics_config = MetricsConfig(app_name="PROD_API", include_trace_exemplar=True)

    sentry_sdk.init(
        dsn="https://e609472d95c9f3e3de39ae25c98baadb@o4508853327888384.ingest.de.sentry.io/4508904557117520",
        send_default_pii=True,
        max_request_body_size='always'
    )

    app = FastAPI(
        lifespan=lifespan,
        root_path="/api",
        root_path_in_servers=True,
        servers=[
            {"url": "https://prod-team-37-ajc3mefd.REDACTED/api"}
        ]
    )

    app.add_middleware(SentryAsgiMiddleware)

    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema
        openapi_schema = get_openapi(
            title="API с JWT авторизацией",
            version="1.0",
            description="Пример API, использующего JWT для авторизации в Swagger UI",
            routes=app.routes,
        )
        openapi_schema["servers"] = [{"url": app.root_path}]
        openapi_schema["components"]["securitySchemes"] = {
            "BearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
                "description": "JWT токен для авторизации. Формат: Bearer <токен>"
            }
        }
        for path in openapi_schema["paths"].values():
            for method in path.values():
                method["security"] = [{"BearerAuth": []}]
        app.openapi_schema = openapi_schema
        return app.openapi_schema

    app.openapi = custom_openapi

    setup_metrics(app=app, config=metrics_config)

    return app


def configure_app(app: FastAPI, root_router: APIRouter, config: Config) -> None:
    app.include_router(root_router)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )

    setup_exception_handlers(app)

    container = create_async_container(get_providers(), config=config)
    setup_dishka(container, app)


def main():
    app = create_app()
    config = create_config()
    configure_app(app, root_router, config)

    host = config.server.SERVER_HOST
    port = config.server.SERVER_PORT

    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    main()
