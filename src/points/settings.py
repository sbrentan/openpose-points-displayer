import os

# Database
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///src/points/database/points_db.db")
