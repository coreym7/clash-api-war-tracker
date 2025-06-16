
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import War
from datetime import datetime

# Connect to your DB
engine = create_engine("sqlite:///clash_tracker.db")
Session = sessionmaker(bind=engine)
session = Session()


wars = session.query(War).order_by(War.id.asc()).all()
for war in wars:
    print(f"ID: {war.id} | Tag: {war.war_tag} | State: {war.state}")
#This was needed becuase discovered running a iteration while war is in prep phase the start time can vary by a few milliseconds, creating a new unique war tag duplicating the war
#Will update fetch data to stop if the war state is in preperation.
# Delete wars by ID
war_ids_to_delete = [3, 4]
wars_to_delete = session.query(War).filter(War.id.in_(war_ids_to_delete)).all()

for war in wars_to_delete:
    print(f"🗑 Deleting War ID: {war.id} | Tag: {war.war_tag}")
    session.delete(war)

session.commit()
print("✅ Deleted specified wars.")