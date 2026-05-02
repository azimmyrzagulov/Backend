#!/usr/bin/env python
import sys
import os

# Add current directory to path so app can be imported
sys.path.insert(0, os.path.dirname(__file__))

import uvicorn
from app.config import settings

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
