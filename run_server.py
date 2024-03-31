import uvicorn
from src.settings import settings
from src.app import app

if __name__ == "__main__":
    uvicorn.run(app,
                host=settings.server_host,
                port=settings.server_port)