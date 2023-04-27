import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Jobs(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'jobs'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    team_leader = sa.Column(sa.Integer, sa.ForeignKey('users.id'))
    job = sa.Column(sa.Text)
    work_size = sa.Column(sa.Integer)
    collaborators = sa.Column(sa.String)
    start_date = sa.Column(sa.Date)
    end_date = sa.Column(sa.Date)
    is_finished = sa.Column(sa.Boolean, default=False)
