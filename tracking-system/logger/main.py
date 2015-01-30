# 13.847300,100.569850

from random import uniform
import requests

flat = round(uniform(13, 14), 6)
flon = round(uniform(100, 101), 6)

print(flat, flon)

r = requests.get('http://localhost:8080/hello')

print(r.status_code)
print(r.text)