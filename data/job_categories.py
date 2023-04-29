import sqlalchemy as sa
from .db_session import SqlAlchemyBase

association_table = sa.Table('association_jobs_to_categories', SqlAlchemyBase.metadata,
                             sa.Column('job', sa.ForeignKey('jobs.id')),
                             sa.Column('category', sa.ForeignKey('categories.id')))


class Category(SqlAlchemyBase):
    __tablename__ = 'categories'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    title = sa.Column(sa.String, nullable=True)
