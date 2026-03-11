#!/usr/bin/env python3
"""
Taxeen Website1 - Run Script
Start the Flask marketing website
"""

import os
import sys

# Add the current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app

if __name__ == "__main__":
    # Get configuration from environment or use defaults
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 5001))
    debug = os.getenv("FLASK_DEBUG", "true").lower() == "true"
    
    print(f"""
╔════════════════════════════════════════════╗
║       Taxeen Website - Marketing Site      ║
╠════════════════════════════════════════════╣
║  Starting server on http://{host}:{port}       ║
║  Debug mode: {str(debug).ljust(5)}                      ║
╚════════════════════════════════════════════╝
    """)
    
    app.run(
        host=host,
        port=port,
        debug=debug
    )
