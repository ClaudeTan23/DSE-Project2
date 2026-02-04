from decimal import Decimal
from datetime import datetime, date

def make_json_safe(data: dict):
    safe = {}

    for k, v in data.items():
        if isinstance(v, Decimal):
            safe[k] = float(v)
        elif isinstance(v, (datetime, date)):
            safe[k] = v.isoformat()
        else:
            safe[k] = v

    return safe
