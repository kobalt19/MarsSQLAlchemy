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


@api.route('/api/jobs/<int:id_>')
def get_one_job(id_):
    session = db_session.create_session()
    job = session.get(Jobs, id_)
    if not job:
        return jsonify({'error': 'Not found'})
    return jsonify({'job': job.to_dict(
        only=('team_leader', 'job', 'work_size', 'start_date', 'end_date', 'is_finished'))})
