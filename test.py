import datetime as dt
import requests

print('1:', requests.get('http://127.0.0.1:8080/api/jobs').json())
print('2:', requests.get('http://127.0.0.1:8080/api/jobs/1').json())
print('3:', requests.get('http://127.0.0.1:8080/api/jobs/555').json())
# print('4:', requests.get('http://127.0.0.1:8080/api/jobs/etbt').json())
print('5:', requests.post('http://127.0.0.1:8080/api/jobs', json={'team_leader': 3, 'job': 'job', 'work_size': 1,
                                                                  'start_date': '2022-03-21', 'end_date': '2022-03-22',
                                                                  'collaborators': '1, 2', 'is_finished': False}).json())
