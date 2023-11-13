from core.configs import settings
from core.database import engine
import models


async def create_tables() -> None:
    # Criar um bloco de contexto assíncrono
    async with engine.begin() as conn:
        # Excluir, caso já (alterações...)
        await conn.run_sync(settings.DBBaseModel.metadata.drop_all)  
        await conn.run_sync(settings.DBBaseModel.metadata.create_all)

if __name__ == '__main__':
    import asyncio
    asyncio.run(create_tables())
