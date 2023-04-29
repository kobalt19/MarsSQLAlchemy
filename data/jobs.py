import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase

association_table = sa.Table('association_users_to_jobs', SqlAlchemyBase.metadata,
                             sa.Column('user', sa.ForeignKey('users.id')), sa.Column('job', sa.ForeignKey('jobs.id')))


class Jobs(SqlAlchemyBase):
    __tablename__ = 'jobs'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    team_leader = sa.Column(sa.Integer, sa.ForeignKey('users.id'))
    job = sa.Column(sa.Text)
    work_size = sa.Column(sa.Integer)
    start_date = sa.Column(sa.Date)
    end_date = sa.Column(sa.Date)
    is_finished = sa.Column(sa.Boolean, default=False)
    category = orm.relationship('Category', secondary='association_jobs_to_categories', backref='jobs')
