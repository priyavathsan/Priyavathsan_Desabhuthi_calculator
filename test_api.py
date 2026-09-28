import urllib.request, json
req = urllib.request.Request(
    'http://127.0.0.1:5000/calculate', 
    data=json.dumps({'date':'20/05/1992','time':'20:00','place':'Chennai, India'}).encode('utf-8'), 
    headers={'Content-Type': 'application/json'}
)
resp = urllib.request.urlopen(req).read().decode('utf-8')
data = json.loads(resp)
with open('result.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
