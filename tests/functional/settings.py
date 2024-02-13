from pydantic import BaseSettings, Field


class Settings(BaseSettings):

    redis_host: str = Field(default='localhost')
    redis_port: int = Field(default=6379)

    elastic_host: str = Field(default='localhost', env='ES_HOST')
    elastic_port: int = Field(default=9200, env='ES_PORT')

    api_host: str = Field('localhost', env='API_HOST')
    api_port: int = Field(default=80)

    max_window_size: int = Field(default=10000)

    page_size: int = Field(default=10, env='DEFAULT_PAGE_SIZE')
    page_number: int = Field(default=1, env='DEFAULT_PAGE_NUMBER')

    cache_lifetime: int = Field(default=60 * 5, env='FILM_CACHE_EXPIRE_IN_SECONDS')

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()

API_URL = f'http://{settings.api_host}:{settings.api_port}/api/v1/'
