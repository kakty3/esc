from sqlalchemy import distinct
from sqlalchemy import and_

from esc_identifier.database.models import Base


def get_author_name_variations(session, author_id: int):
    PaperAuthor = Base.metadata.tables['paperauthor']
    TrainConfirmed = Base.metadata.tables['trainconfirmed']

    name_variations = (
        session.query(distinct(PaperAuthor.c.name))
        .select_from(TrainConfirmed)
        .join(PaperAuthor,
              and_(PaperAuthor.c.authorid == TrainConfirmed.c.authorid,
                   PaperAuthor.c.paperid == TrainConfirmed.c.paperid))
        .filter(TrainConfirmed.c.authorid == author_id)
        .all()
    )

    return [i[0] for i in name_variations]


def get_affiliation_variants(session, author_id):
    PaperAuthor = Base.metadata.tables['paperauthor']
    TrainConfirmed = Base.metadata.tables['trainconfirmed']

    affiliation_variations = (
        session.query(distinct(PaperAuthor.c.affiliation))
        .select_from(TrainConfirmed)
        .join(PaperAuthor,
              and_(PaperAuthor.c.authorid == TrainConfirmed.c.authorid,
                   PaperAuthor.c.paperid == TrainConfirmed.c.paperid))
        .filter(TrainConfirmed.c.authorid == author_id)
        .filter(PaperAuthor.c.affiliation != '')
        .all()
    )

    return [i[0] for i in affiliation_variations]


def get_trainconfirmed_authors_ids(session):
    TrainConfirmed = Base.metadata.tables['trainconfirmed']

    authors_ids = (
        session.query(TrainConfirmed.c.authorid)
        .distinct()
        .all()
    )

    return [i[0] for i in authors_ids]
