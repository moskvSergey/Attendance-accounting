from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from data.db_session import SqlAlchemyBase


class Attendance(SqlAlchemyBase):
    __tablename__ = 'attendance'

    id = Column(Integer, primary_key=True, autoincrement=True)
    lesson_id = Column(Integer, ForeignKey('lessons.id'))
    lesson = relationship("Lesson")
    person_id = Column(Integer, ForeignKey('people.id'))
    person = relationship("Person")