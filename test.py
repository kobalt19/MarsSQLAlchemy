import datetime as dt
import requests

print('1:', requests.get('http://127.0.0.1:8080/api/jobs').json())
print('2:', requests.get('http://127.0.0.1:8080/api/jobs/1').json())
print('3:', requests.get('http://127.0.0.1:8080/api/jobs/555').json())
print('4:', requests.get('http://127.0.0.1:8080/api/jobs/etbt').json())
print('5:', requests.post('http://127.0.0.1:8080/api/jobs/',
                          json={'id': 5, 'team_leader': 1, 'job': 'w1', 'work_size': 20,
                                'start_date': dt.datetime.now().date().isoformat(),
                                'end_date': dt.date(year=2023, month=5, day=1).isoformat(),
                                'is_finished': False}).json())
