from sqlalchemy import Column, Integer, String
from data.db_session import SqlAlchemyBase
from sqlalchemy.orm import relationship


class Groups(SqlAlchemyBase):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    people = relationship("Person", back_populates="group")