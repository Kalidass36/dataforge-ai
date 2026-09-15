import requests
import json

def main():
    url = "http://127.0.0.1:8000/api/v1/query"
    payload = {"question": "Show me the top 5 customers by spending"}

    r = requests.post(url, json=payload, timeout=120)
    print(r.status_code)
    try:
        print(json.dumps(r.json(), indent=2))
    except Exception:
        print(r.text)


if __name__ == '__main__':
    main()
