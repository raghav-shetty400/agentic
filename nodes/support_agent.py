from tools.user_tool import get_user
from tools.device_tool import get_device
from tools.event_tool import get_events
from tools.subscription_tool import get_subscription
from tools.settings_tool import get_settings

from concurrent.futures import ThreadPoolExecutor

import json
import time


def support_agent(state):

    total_start = time.time()

    # =====================================================
    # USER
    # =====================================================

    start = time.time()

    user = get_user(state["username"])

    print(
        f"get_user(): {time.time() - start:.2f} sec"
    )

    if user is None:

        return {
            **state,
            "answer": "Username not found."
        }


    # =====================================================
    # DEVICE
    # =====================================================

    start = time.time()

    device = get_device(user["id"])

    print(
        f"get_device(): {time.time() - start:.2f} sec"
    )

    if device is None:

        return {
            **state,
            "answer": "No device found."
        }


    # =====================================================
    # PARALLEL CALLS
    # =====================================================

    parallel_start = time.time()

    with ThreadPoolExecutor(max_workers=3) as executor:

        # Start all three calls at the same time

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


        # Wait for results

        subscription = subscription_future.result()

        settings = settings_future.result()

        events = events_future.result()


    print(
        f"Parallel calls TOTAL: "
        f"{time.time() - parallel_start:.2f} sec"
    )


    # =====================================================
    # ATTRIBUTES
    # =====================================================

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


    # =====================================================
    # LATEST ROLLOVER EVENT
    # =====================================================

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


    # =====================================================
    # BUILD SUPPORT REPORT
    # =====================================================

    answer = f"""
I investigated your rollover issue.

👤 User

Name : {user['name']}
Email : {user['email']}

📷 Device

MAC Address : {device['mac_address']}
Plan : {device['plan_id']}
Firmware : {device['firmware_version']}
Registration : {device['registration_id']}

🔄 Rollover

Enabled : {'Yes' if rollover == 1 else 'No'}
Latest State : {rollover_state}

📦 Subscription

{'Found' if subscription else 'Not Found'}

⚙ Device Settings

{len(settings)} settings found.

📡 Latest Event

{'Found' if latest_event else 'Not Found'}
"""


    # =====================================================
    # TOTAL TIME
    # =====================================================

    print(
        f"support_agent TOTAL: "
        f"{time.time() - total_start:.2f} sec"
    )


    # =====================================================
    # RETURN STATE
    # =====================================================

    return {
        **state,
        "answer": answer
    }