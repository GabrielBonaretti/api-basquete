from pydantic.v1 import BaseSettings
from sqlalchemy.orm import declarative_base


class Settings(BaseSettings):
    """
        Configurações gerais ultilizadas em nossa aplicação!
    """

    API_V1_STR: str = '/api/v1'  # Não precisar inserir via hard coding

    # ideal
    # DB_URL: str = 'mysql+asyncmy://user:senha@127.0.0.1:3306/etscursos'
    DB_URL: str = 'mysql+asyncmy://root@127.0.0.1:3306/basketball'

    DBBaseModel = declarative_base()  # Serve para que os models gerdem todos os recursos do sqlalchemy

    class Config:
        case_sensitive = True


settings = Settings()  # Declarando a variavel aqui, em qualquer lugar que eu import o arquivo terei acesso a essas configs