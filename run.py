import sys
import os

# Ensure src is on sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from agentic_data_storyteller.cli import main

if __name__ == "__main__":
    main()
