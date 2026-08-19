def ask_username(state):

    print(">>> ask_username")
    print(state)

    # =================================================
    # USERNAME / EMAIL ALREADY PROVIDED
    # =================================================

    if state.get("username"):

        return {
            **state,
            "answer": ""
        }

    # =================================================
    # GET DETECTED INTENT
    # =================================================

    intent = state.get(
        "intent",
        "support"
    )

    # =================================================
    # ASK FOR USERNAME / EMAIL
    # =================================================

    return {
        **state,
        "answer": (
            f"Sure! I can help you investigate the "
            f"{intent} issue.\n\n"
            "Before I proceed, please enter your "
            "username or email address."
        )
    }