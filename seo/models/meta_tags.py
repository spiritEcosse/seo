from typing import List

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import INTEGER, TEXT, JSONB
from sqlalchemy.orm import Session
from sqlalchemy.orm.query import Query

from seo.database import db
from seo.background import run_async
from seo.logger import get_logger


__all__ = [
    "MetaTags",
]


_logger = get_logger()


class MetaTags(db.BaseModel):
    """
    Data model for Example DB table.
    """
    __tablename__ = 'meta_tags'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    slug = Column(TEXT, nullable=False, index=True, unique=True)
    title = Column(TEXT, nullable=False)
    description = Column(TEXT, nullable=False)
    data = Column(JSONB, nullable=False)

    def __init__(self, id_, slug, title, description, data):
        """
        New model instance initializer
        :param name: the name of the example
        """
        self.id = id_
        self.slug = slug
        self.title = title
        self.description = description
        self.data = data

    @classmethod
    async def get_by_id(cls, id_: str, session: Session) -> "Query":
        """
        Returns a record by ID

        :param id_: stringified UUID, i.e.: str(uuid_object)
        :param session: SQLAlchemy database session
        :return: THe specified Example by id or None
        """
        ###
        # Run the SQLAlchemy session.query(MetaTags).get() function in the background
        #
        return await run_async(session.query(cls).get, (id_,))

    @classmethod
    async def get_by_slug(cls, slug: str, session: Session) -> "Query":
        """
        Returns a record by slug

        :param slug: string, i.e.: /avto/polsha/
        :param session: SQLAlchemy database session
        :return: THe Query
        """
        ###
        # Run the SQLAlchemy session.query(MetaTags).filter_by() function in the background
        #
        return await run_async(session.query(cls).filter_by, **{"slug": slug})

    @classmethod
    async def first(cls, session: Session) -> "Query":
        """
        Returns first record

        :param session: SQLAlchemy database session
        :return: THe specified Example by id or None
        """
        ###
        # Run the SQLAlchemy session.query(MetaTags).first() function in the background
        #
        return await run_async(session.query(cls).first)

    @classmethod
    async def get_all(cls, session: Session) -> List["MetaTags"]:
        """
        Returns all records in the table

        :param session: SQLAlchemy database session
        :return: List of all examples in the database
        """
        ###
        # Run the SQLAlchemy session.query(Example).all() function in the background
        #
        return await run_async(session.query(cls).all)

    @classmethod
    async def delete_all(cls, session: Session) -> int:
        """
        Delete all records in the table

        :param session: SQLAlchemy database session
        :return: int : the count of rows matched as returned by the database's "row count" feature.
        """
        ###
        # Run the SQLAlchemy session.query(Example).delete() function in the background
        #
        return await run_async(session.query(cls).delete)

    @property
    def serialized(self):
        return {
            "slug": self.slug,
            "title": self.title,
            "description": self.description,
            "data": self.data,
        }
