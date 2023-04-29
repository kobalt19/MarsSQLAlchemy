from flask import Blueprint, jsonify
from . import db_session
from .jobs import Jobs

api = Blueprint('jobs_api', __name__, template_folder='templates')


@api.route('/api/jobs')
def get_all_jobs():
    session = db_session.create_session()
    all_jobs = session.query(Jobs).all()
    return jsonify({'jobs': [job.to_dict(
        only=('team_leader', 'job', 'work_size', 'start_date', 'end_date', 'is_finished')
    ) for job in all_jobs]})
