from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

# ✅ Database URL (SQLite in this case)
DATABASE_URL = "sqlite:///./users.db"

# ✅ Define ORM Base Class
Base = declarative_base()

# ✅ Define User Model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)

# ✅ Create Database Engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# ✅ Create Session Local Class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ✅ Function to Initialize Database (Create Tables)
def init_db():
    Base.metadata.create_all(bind=engine)

# ✅ Dependency to Get Database Session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
