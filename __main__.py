from webscrapping import webscrape
from settings import set_os

webscrape('Pune', '', 2, set_os('windows'))

ts = []
for i in range(5):
    ts.append(webscrape('Pune', '', i, set_os('windows')))

for t in ts:
    t.start()

for t in ts:
    t.join()

print('Ok we have finished webscrapping')