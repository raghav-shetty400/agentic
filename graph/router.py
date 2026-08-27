def router(state):

    question = state.get(
        "question",
        ""
    ).lower().strip()


    print()
    print("========== ROUTER ==========")
    print("Question :", question)
    print("Username :", state.get("username", ""))
    print("Route IN :", state.get("route", ""))
    print("Intent IN:", state.get("intent", ""))
    print("============================")


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