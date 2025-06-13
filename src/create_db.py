from sqlalchemy import create_engine
from models import Base

engine = create_engine("sqlite:///clash_tracker.db")
Base.metadata.create_all(engine)

print("Database created as clash_tracker.db")