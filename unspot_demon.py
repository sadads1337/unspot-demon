import functools
import logging
import os
import time

import requests
import schedule

from typing import Any


def catch_exceptions(cancel_on_failure=False):
    def catch_exceptions_decorator(job_func):
        @functools.wraps(job_func)
        def wrapper(*args, **kwargs):
            # noinspection PyBroadException
            try:
                return job_func(*args, **kwargs)
            except Exception:
                import traceback
                logging.error(traceback.format_exc())
                if cancel_on_failure:
                    return schedule.CancelJob
        return wrapper
    return catch_exceptions_decorator


def _env_safe(name: str, error: str = "") -> Any:
    if name not in os.environ:
        logging.error(f"No env variable with name '{name}'. {error}")
        return None
    return os.environ[name]


def _make_base_header(secret: str, content_type: str = "application/json") -> dict:
    return {"Content-Type": content_type, "Authorization": f"Bearer {secret}"}


@catch_exceptions(cancel_on_failure=False)
def _auto_approve(end_point, secret: str):
    checkin_list_resp = requests.get(f"{end_point}/api/bookings/checkin-available-list?select=",
                                     headers=_make_base_header(secret))
    if not checkin_list_resp:
        logging.error("Unable to obtain checkin list")

    for booking in checkin_list_resp.json()["body"]["bookings"]:
        booking_id = booking["id"]
        checkin_resp = requests.patch(f"{end_point}/api/bookings/{booking_id}/checkin",
                                      headers=_make_base_header(secret))
        if not checkin_resp:
            logging.error(f"Unable to checkin booking {booking_id}")
        else:
            spaces = ",".join([space["name"] for space in booking["spaces"]])
            logging.info(f"Checked in id: '{booking_id}' spaces:'{spaces}'")


def _main() -> int:
    end_point = _env_safe("UNSPOT_ENDPOINT", "No end point found, specify it via env var 'UNSPOT_ENDPOINT'")
    secret = _env_safe("UNSPOT_SECRET", "No secret found, specify it via env var 'UNSPOT_SECRET'")
    if not all([end_point, secret]):
        return -1

    schedule.every(5).to(10).minutes.do(_auto_approve, end_point, secret)

    while True:
        secs = schedule.idle_seconds()
        if secs is None:
            break
        elif secs > 0:
            time.sleep(secs)
        schedule.run_pending()


if __name__ == "__main__":
    _main()
