#!/usr/bin/env python3
"""
Taxeen Frontend1 - Run Script
Start the Flask application server
"""

import os
import sys

# Add the current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app

if __name__ == "__main__":
    # Get configuration from environment or use defaults
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "true").lower() == "true"
    
    print(f"""
╔════════════════════════════════════════════╗
║       Taxeen Frontend - Flask App          ║
╠════════════════════════════════════════════╣
║  Starting server on http://{host}:{port}       ║
║  Debug mode: {str(debug).ljust(5)}                      ║
║  API URL: {os.getenv('API_BASE_URL', 'http://localhost:8000/api')[:30].ljust(30)} ║
╚════════════════════════════════════════════╝
    """)
    
    app.run(
        host=host,
        port=port,
        debug=debug
    )
