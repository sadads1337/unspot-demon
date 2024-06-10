# UnSpot Auto Approve
Helper script to auto approve bookings in [UnSpot](https://unspot.ru).

## Quick Start
1) Install dependencies if need `pip3 install -r requirements.txt`
2) Add execute permissions `chmod +x unspot_demon.py`
3) Set environment variables:
   - `UNSPOT_ENDPOINT` - Endpoint for API,
   - `UNSPOT_SECRET` - Bearer secret for auth [help-center/faq/api/](https://unspot.ru/help-center/faq/api/)
4) Run script in background `nohup python3 unspot_demon.py &` and `ps ax | grep unspot_demon.py`

## Requirements

Python 3.8+

- requests >= 2.32
- schedule >= 1.2
