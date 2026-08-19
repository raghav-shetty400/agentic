from typing import TypedDict


class AgentState(TypedDict, total=False):

    # ---------------- USER QUESTION ----------------

    question: str

    # ---------------- USER DETAILS ----------------

    username: str

    user: dict

    # ---------------- DEVICE DETAILS ----------------

    device: dict

    # ---------------- SUBSCRIPTION ----------------

    subscription: dict

    # ---------------- DEVICE SETTINGS ----------------

    settings: list

    # ---------------- EVENTS ----------------

    events: list

    # ---------------- RESPONSE ----------------

    answer: str

    # ---------------- ROUTING ----------------

    route: str

    # ---------------- INTENT ----------------

    intent: str