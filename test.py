import pandas as pd
from sqlalchemy import create_engine, inspect

# PostgreSQL connection string
POSTGRES_URL = "postgresql+psycopg2://test_user:test_password@localhost:6000/test_db"
# SQLite connection string
SQLITE_URL = "sqlite:///sqlite.db"

# Create SQLAlchemy engines
postgres_engine = create_engine(POSTGRES_URL)
sqlite_engine = create_engine(SQLITE_URL)

# List of tables to transfer
tables = ['news', 'category', 'source', 'url', 'user', 'view']

# Loop through each table and transfer data
for table in tables:
    # Read data from PostgreSQL table
    df = pd.read_sql_table(table, postgres_engine)
    
    # Write data to SQLite table
    df.to_sql(table, sqlite_engine, if_exists='replace', index=False)

print("Data transfer complete.")
