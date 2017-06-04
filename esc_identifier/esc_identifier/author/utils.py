from . import Author, RealAuthor


def to_real_author(author: Author) -> RealAuthor:
    return RealAuthor(
        kdd_author_ids=[author.kdd_id],
        name=author.name,
        affiliation=author.affiliation
    )
