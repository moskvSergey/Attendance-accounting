from sqlalchemy import Column, Integer, String
from data.db_session import SqlAlchemyBase


class Person(SqlAlchemyBase):
    __tablename__ = 'people'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)