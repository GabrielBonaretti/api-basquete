from fastapi import FastAPI
from core.configs import settings
from api.v1._api import api_router

tags_metadata = [
    {
        "name": "teams",
        "description": "All endpoints that get teams.",
    },
    {
        "name": "leagues",
        "description": "Manage leagues.",
    },
]

# create app Fastapi
app = FastAPI(
    title='API de Cursos da ETS',
    openapi_tags=tags_metadata
)


app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host='0.0.0.0', port=8001,
                log_level='info', reload=True)
