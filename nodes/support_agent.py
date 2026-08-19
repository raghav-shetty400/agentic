from tools.device_tool import get_device
from tools.event_tool import get_events
from tools.subscription_tool import get_subscription
from tools.settings_tool import get_settings

from concurrent.futures import ThreadPoolExecutor

import json
import time


def support_agent(state):

    total_start = time.time()

    # =================================================
    # USER
    # =================================================

    user = state.get("user")

    if user is None:

        return {
            **state,
            "answer": "User verification failed."
        }

    # =================================================
    # DEVICE
    # =================================================

    start = time.time()

    device = get_device(user["id"])

    print(
        f"get_device(): "
        f"{time.time() - start:.2f} sec"
    )

    if device is None:

        return {
            **state,
            "answer": "No device found."
        }

    # =================================================
    # PARALLEL DATABASE / API CALLS
    # =================================================

    start = time.time()

    with ThreadPoolExecutor(max_workers=3) as executor:

        subscription_future = executor.submit(
            get_subscription,
            device["id"]
        )

        settings_future = executor.submit(
            get_settings,
            device["id"]
        )

        events_future = executor.submit(
            get_events,
            user["authentication_token"]
        )

        subscription = subscription_future.result()
        settings = settings_future.result()
        events = events_future.result()

    print(
        f"Parallel calls TOTAL: "
        f"{time.time() - start:.2f} sec"
    )

    # =================================================
    # ATTRIBUTES
    # =================================================

    attributes = device.get("attributes", {})

    if isinstance(attributes, bytes):

        attributes = attributes.decode("utf-8")

    if isinstance(attributes, str):

        try:

            attributes = json.loads(attributes)

        except json.JSONDecodeError:

            attributes = {}

    if not isinstance(attributes, dict):

        attributes = {}

    rollover = attributes.get("rollover", 0)

    # =================================================
    # ROLLOVER EVENT
    # =================================================

    latest_event = None

    rollover_state = "No rollover event"

    for event in events:

        if str(event.get("alert")) == "4":

            latest_event = event

            rollover_state = event.get(
                "rolloverState",
                "Unknown"
            )

            break

    # =================================================
    # REPORT
    # =================================================

    answer = f"""
I investigated your {state.get("intent", "support")} issue.

👤 User

Name : {user.get("name")}
Email : {user.get("email")}

📷 Device

MAC Address : {device.get("mac_address")}
Plan : {device.get("plan_id")}
Firmware : {device.get("firmware_version")}
Registration : {device.get("registration_id")}

🔄 Rollover

Enabled : {"Yes" if rollover == 1 else "No"}
Latest State : {rollover_state}

📦 Subscription

{"Found" if subscription else "Not Found"}

⚙ Device Settings

{len(settings)} settings found.

📡 Latest Event

{"Found" if latest_event else "Not Found"}
"""

    print(
        f"support_agent TOTAL: "
        f"{time.time() - total_start:.2f} sec"
    )

    return {
        **state,
        "device": device,
        "subscription": subscription,
        "settings": settings,
        "events": events,
        "answer": answer
    }