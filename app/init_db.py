from src import models
from src.database import session

"""
Initialize the database by creating all the tables defined in the models.

This script should be executed to create the necessary tables in the database before running the application.

Usage:
    python init_db.py

Note:
    - The script imports the models and the database session from the src package.
    - The function `init_db()` creates all the tables defined in the models.
    - The script should be executed as the main module to initialize the database.
"""

def init_db():
    models.Base.metadata.create_all(bind=session.engine)

if __name__ == "__main__":
    init_db()

