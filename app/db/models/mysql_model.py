from sqlalchemy import Column, Integer, String
from app.db.base import Base

class MySQLModel(Base):
    __tablename__ = "mysql_table"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)
