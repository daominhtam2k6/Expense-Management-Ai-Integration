from sqlalchemy import inspect, text
from sqlalchemy.engine import Engine


def ensure_category_icon_column(engine: Engine) -> None:
    """Add and backfill the category icon column for databases created before it existed."""
    inspector = inspect(engine)
    if "categories" not in inspector.get_table_names():
        return

    columns = {column["name"] for column in inspector.get_columns("categories")}
    if "icon" in columns:
        return

    with engine.begin() as connection:
        connection.execute(
            text(
                "ALTER TABLE categories "
                "ADD COLUMN icon VARCHAR NOT NULL DEFAULT 'circle-dollar-sign'"
            )
        )
        connection.execute(
            text(
                "UPDATE categories "
                "SET icon = CASE WHEN type = 'income' THEN 'banknote' ELSE 'wallet' END"
            )
        )
