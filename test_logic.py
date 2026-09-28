import json
from logic import calculate_dasa_bhukti
res = calculate_dasa_bhukti("1992/05/20", "20:00", 13.0827, 80.2707)
with open('result_direct.json', 'w', encoding='utf-8') as f:
    json.dump(res, f, indent=2, ensure_ascii=False)
