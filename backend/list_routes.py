
from app import app
import json

def list_cancel_routes():
    routes = []
    for rule in app.url_map.iter_rules():
        if "photographer-cancel" in str(rule) or "cancellation-check" in str(rule) or "status" in str(rule):
            routes.append({
                "endpoint": rule.endpoint,
                "methods": list(rule.methods),
                "rule": str(rule)
            })
    
    print(json.dumps(routes, indent=2))

if __name__ == "__main__":
    list_cancel_routes()
