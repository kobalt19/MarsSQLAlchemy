import datetime as dt
from flask import Blueprint, jsonify, request
from . import db_session
from .jobs import Jobs

api = Blueprint('jobs_api', __name__, template_folder='templates')


@api.route('/api/jobs', methods={'GET'})
def get_all_jobs():
    session = db_session.create_session()
    all_jobs = session.query(Jobs).all()
    return jsonify({'jobs': [job.to_dict(
        only=('team_leader', 'job', 'work_size', 'start_date', 'end_date', 'is_finished')
    ) for job in all_jobs]})


@api.route('/api/jobs/<id_>', methods={'GET'})
def get_one_job(id_):
    if not id_.isdigit():
        return jsonify({'error': 'Bad request'})
    session = db_session.create_session()
    job = session.get(Jobs, id_)
    if not job:
        return jsonify({'error': 'Not found'})
    return jsonify({'job': job.to_dict(
        only=('team_leader', 'job', 'work_size', 'start_date', 'end_date', 'is_finished'))})


@api.route('/api/jobs/', methods={'POST'})
def add_job():
    session = db_session.create_session()
    if not request.json:
        return jsonify({'error': 'No request'})
    if not all(key in request.json for key in
               {'id', 'team_leader', 'job', 'work_size', 'start_date', 'end_date', 'is_finished'}):
        return jsonify({'error': 'Bad request'})
    if session.get(Jobs, request.json['id']):
        return jsonify({'error': 'Id already exists'})
    try:
        job = Jobs(
            id=request.json['id'],
            team_leader=request.json['team_leader'],
            job=request.json['job'],
            work_size=request.json['work_size'],
            start_date=dt.datetime.fromisoformat(request.json['start_date']).date(),
            end_date=dt.datetime.fromisoformat(request.json['end_date']).date(),
            is_finished=request.json['is_finished'],
        )
        session.add(job)
        session.commit()
    except BaseException as err:
        session.rollback()
        raise err
    return jsonify({'success': 'OK'})
