from database import engine
from app.models.models import Base
Base.metadata.create_all(bind=engine)

