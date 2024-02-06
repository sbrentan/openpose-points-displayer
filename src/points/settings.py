import os

# Database
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///src/points/database/points_db.db")

# Documents Folder
DOCUMENTS_FOLDER = os.getenv("DOCUMENTS_FOLDER", "src/points/documents")
