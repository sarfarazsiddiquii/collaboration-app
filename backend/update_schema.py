from extensions import db
from app import app
from sqlalchemy import text

# Create a new column in the workspace table with a default value
with app.app_context():
    with db.engine.connect() as connection:
        connection.execute(text('ALTER TABLE workspace ADD COLUMN plain_code VARCHAR(128) NOT NULL DEFAULT "";'))
    print("Database schema updated successfully.")