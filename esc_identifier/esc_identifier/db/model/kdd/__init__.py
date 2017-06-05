from sqlalchemy import (
    Column, Integer, String,
)
from sqlalchemy.schema import PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base

from esc_identifier.db.utils import db_model_repr

Base = declarative_base()
Base.__repr__ = db_model_repr


class Paper(Base):
    __tablename__ = 'paper'

    id = Column(Integer, primary_key=True, unique=True)
    title = Column(String)
    year = Column(Integer)
    conferenceid = Column(Integer)
    journalid = Column(Integer)
    keyword = Column(String)


class PaperAuthor(Base):
    __tablename__ = 'paperauthor'

    paperid = Column(Integer)
    authorid = Column(Integer)
    name = Column(String)
    affiliation = Column(String)

    __table_args__ = (PrimaryKeyConstraint(paperid, authorid),)
