from requests import get, post, delete

print(get('http://localhost:5000/api/v2/groups').json())


print(get('http://localhost:5000/api/v2/groups/4').json())

print(get('http://localhost:5000/api/v2/groups/999').json())
# новости с id = 999 нет в базе


print(post('http://localhost:5000/api/v2/groups').json())
print(post('http://localhost:5000/api/v2/groups',
           json={'name': 'reggg2004@mail.ru'}).json())
print(post('http://localhost:5000/api/v2/groups',
           json={}).json())



print(delete('http://localhost:5000/api/v2/groups/999').json())
# новости с id = 999 нет в базе

print(delete('http://localhost:5000/api/v2/groups/4').json())