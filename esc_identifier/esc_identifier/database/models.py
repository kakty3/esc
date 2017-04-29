from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class Record(Base):
    # TODO: rename to `record`
    __tablename__ = 'records'

    id = Column(Integer, primary_key=True)
    pmid = Column(Integer, unique=True)
    title = Column(String, nullable=False)
    abstract = Column(String, nullable=False)

    authors = relationship('Author', backref='record')

    def __repr__(self):
        return (f'Record<id={self.id}, '
                f'pmid={self.pmid}, '
                f'title={self.title}>')


class Author(Base):
    # TODO: rename to `author`
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True)
    fore_name = Column(String(100), nullable=False)
    last_name = Column(String(100))

    record_id = Column(Integer, ForeignKey('records.id'))

    def to_str(self):
        if not self.last_name:
            return self.fore_name

        return f'{self.fore_name} {self.last_name}'

    def __repr__(self):
        return (f'Author<id={self.id}, '
                f'last_name={self.last_name}, '
                f'fore_name={self.fore_name}>')
