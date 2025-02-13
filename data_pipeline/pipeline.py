from sqlalchemy import create_engine
from sqlalchemy import text

db_path = "/data_pipeline/globo.db"
engine = create_engine(f"sqlite://{db_path}", echo=True)

with engine.connect() as conn:
    result = conn.execute(text("select 'hello world'"))
    print(result.all())