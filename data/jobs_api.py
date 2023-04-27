import datetime as dt
from flask import Blueprint, jsonify, request
from . import db_session
from .jobs import Jobs

blueprint = Blueprint('jobs_api', __name__, template_folder='templates', url_prefix='/api/jobs/')


@blueprint.route('/')
def get_jobs():
    session = db_session.create_session()
    jobs = session.query(Jobs).all()
    if jobs:
        return jsonify({'jobs': [i.to_dict(only=('id', 'team_leader', 'job')) for i in jobs]})
    return {'error': 'Error in database'}


@blueprint.route('/<int:job_id>/')
def get_one_job(job_id):
    session = db_session.create_session()
    job = session.query(Jobs).get(job_id)
    if not job:
        return {'error': 'Error in database'}
    return jsonify({'jobs': job.to_dict(only=('id', 'team_leader', 'job'))})


@blueprint.route('/', methods={'POST'})
def create_job():
    session = db_session.create_session()
    if not request.json:
        return jsonify({'error': 'Empty request'})
    if not all(key in request.json for key in {'team_leader', 'job', 'work_size', 'collaborators', 'start_date',
                                               'end_date'}):
        return jsonify({'error': 'Bad request'})
    if session.query(Jobs).filter(Jobs.id == request.json['id']).first():
        return jsonify({'error': 'Id already exists'})
    job = Jobs(
        id=request.json['id'],
        team_leader=request.json['team_leader'],
        job=request.json['job'],
        work_size=request.json['work_size'],
        collaborators=request.json['collaborators'],
        start_date=dt.datetime.fromisoformat(request.json['start_date']),
        end_date=dt.datetime.fromisoformat(request.json['end_date']),
        is_finished=request.json['is_finished']
    )
    session.add(job)
    session.commit()
    return jsonify({'success': 'OK'})
