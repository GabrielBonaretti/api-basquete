from fastapi import FastAPI
from routers.leagues import router as router_leagues 
from routers.teams import router as router_teams

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

# create app FASTAPI
app = FastAPI(openapi_tags=tags_metadata)

app.include_router(router_teams)
app.include_router(router_leagues)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', host="127.0.0.1", port=8011, log_level="info", reload=True)

