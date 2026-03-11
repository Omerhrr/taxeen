#!/usr/bin/env python3
"""
Taxeen Backend - Run Script
Start the FastAPI server with Uvicorn
"""

import uvicorn
import os
import sys

# Add the current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    # Get configuration from environment or use defaults
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    debug = os.getenv("DEBUG", "true").lower() == "true"
    
    print(f"""
╔════════════════════════════════════════════╗
║       Taxeen Backend API Server            ║
╠════════════════════════════════════════════╣
║  Starting server on http://{host}:{port}       ║
║  Debug mode: {str(debug).ljust(5)}                      ║
║  API Docs: http://{host}:{port}/docs        ║
╚════════════════════════════════════════════╝
    """)
    
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=debug,
        log_level="info"
    )
