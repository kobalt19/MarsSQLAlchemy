import requests

print('1:', requests.get('http://127.0.0.1:8080/api/jobs/').json())
print('2:', requests.get('http://127.0.0.1:8080/api/jobs/1').json())
print('3:', requests.get('http://127.0.0.1:8080/api/jobs/555').json())
print('4:', requests.get('http://127.0.0.1:8080/api/jobs/etbt').json())
