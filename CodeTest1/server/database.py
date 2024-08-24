from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import declarative_base, sessionmaker

# Update the DATABASE_URL to connect to PostgreSQL
DATABASE_URL = "postgresql://tofutest:1234@localhost:5432/partdata"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
'''try:
    with engine.connect() as connection:
        print("เชื่อมต่อฐานข้อมูล PostgreSQL สำเร็จ")
except Exception as e:
    print(f"ไม่สามารถเชื่อมต่อฐานข้อมูล PostgreSQL: {e}")'''
Base = declarative_base()
