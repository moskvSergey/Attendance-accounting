from sqlalchemy import Column, Integer, String, JSON, ForeignKey
from data.db_session import SqlAlchemyBase
from sqlalchemy.orm import relationship


class Person(SqlAlchemyBase):
    __tablename__ = 'people'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    face_vector = Column(JSON, nullable=False)
    group_id = Column(Integer, ForeignKey('groups.id'))
    group = relationship("Groups", back_populates="people")