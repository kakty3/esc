from sqlalchemy import (
    Column, Integer, String
)
from sqlalchemy.schema import (
    PrimaryKeyConstraint, ForeignKey
)
from sqlalchemy.orm import relationship
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


class Author(Base):
    __tablename__ = 'author'

    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String)
    affiliation = Column(String)


class PaperAuthor(Base):
    __tablename__ = 'paperauthor'

    paperid = Column(Integer, ForeignKey('paper.id'))
    paper = relationship("Paper", backref="paperauthor")

    authorid = Column(Integer, ForeignKey('author.id'))
    author = relationship("Author", backref="paperauthor")

    name = Column(String)
    affiliation = Column(String)

    __table_args__ = (PrimaryKeyConstraint(paperid, authorid),)
