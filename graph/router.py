def router(state):

    question = state.get(
        "question",
        ""
    ).lower().strip()

    route_in = state.get(
        "route",
        ""
    )

    intent_in = state.get(
        "intent",
        ""
    )

    print()
    print("========== ROUTER ==========")
    print("Question :", question)
    print("Username :", state.get("username", ""))
    print("Route IN :", route_in)
    print("Intent IN:", intent_in)
    print("============================")


    # =====================================================
    # ALREADY SUPPORT
    # =====================================================

    if route_in == "support":

        print()
        print(">>> EXISTING SUPPORT FLOW")
        print(">>> Route  : support")
        print(">>> Intent :", intent_in or question)

        return {
            **state,
            "route": "support",
            "intent": intent_in or question
        }


    # =====================================================
    # SUPPORT KEYWORDS
    # =====================================================

    support_words = [

        "rollover",
        "roll over",

        "flip",
        "cry",
        "sleep",

        "motion",
        "motion alert",
        "false alert",

        "firmware",

        "subscription",
        "plan",

        "camera",
        "camera issue",

        "offline",

        "device",
        "device issue",

        "sensor",
        "sensors",

        "notification",
        "notifications",

        "battery",

        "registration",

        "installation",
        "setup"

    ]


    # =====================================================
    # DETECT SUPPORT
    # =====================================================

    for word in support_words:

        if word in question:

            print()
            print(">>> SUPPORT DETECTED")
            print(">>> Keyword :", word)
            print(">>> Route    : support")
            print(">>> Intent   :", word)

            return {
                **state,
                "route": "support",
                "intent": word
            }


    # =====================================================
    # GENERAL
    # =====================================================

    print()
    print(">>> GENERAL CHAT")
    print(">>> Route : rag")

    return {
        **state,
        "route": "rag",
        "intent": "general"
    }