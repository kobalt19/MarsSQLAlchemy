import sqlalchemy as sa
from sqlalchemy import orm
from .db_session import SqlAlchemyBase

association_table = sa.Table('association_users_to_deps', SqlAlchemyBase.metadata,
                             sa.Column('department', sa.ForeignKey('departments.id')),
                             sa.Column('user', sa.ForeignKey('users.id')))


class Department(SqlAlchemyBase):
    __tablename__ = 'departments'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    title = sa.Column(sa.String, nullable=True)
    chief_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'))
    email = sa.Column(sa.String, nullable=True)
    chief = orm.relationship('User')
