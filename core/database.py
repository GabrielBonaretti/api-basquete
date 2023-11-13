from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession
from core.configs import settings

# import sys
# default_path = r"C:\\Users\\ct67ca\\Desktop\\base-fastapi"
# sys.path.append(default_path)

engine: AsyncEngine = create_async_engine(settings.DB_URL)

# Sessionmaker retorna uma classe para nós!
# Ele que vai abrir e fechar a conexão com nosso banco de dados!
Session: AsyncSession = sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession,
    bind=engine
)
