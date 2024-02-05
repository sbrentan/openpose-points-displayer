from common.database.sqlite import SqliteDatabase
from points.database.collections.document import CSVDocumentCollection
from points.settings import DATABASE_URL


class PointsDatabase(SqliteDatabase):
    document: CSVDocumentCollection
    database_url = DATABASE_URL


points_database = PointsDatabase()


async def get_db():
    try:
        points_database.start()
        yield points_database
        points_database.commit()
    finally:
        # Close the database connection when the request is done
        points_database.close()
