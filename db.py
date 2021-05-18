import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://nzfbystkzmbbli:02285b405cc74f4819c120ee947030d598c58c90226092e93d32d78ac5d56607" \
                          "@ec2-54-220-53-223.eu-west-1.compute.amazonaws.com:5432/d6rtp4j4g86dr5"#os.getenv("SQLALCHEMY_DATABASE_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()