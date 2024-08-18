from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    mongodb_host: str = 'localhost'
    mongodb_port: int = 27017
    mongodb_database: str = 'myDatabase'

    @property
    def mongodb_uri(self) -> str:
        return f'mongodb://{self.mongodb_host}:{self.mongodb_port}/{self.mongodb_database}'

settings = Settings()