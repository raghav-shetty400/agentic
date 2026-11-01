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
    # SUPPORT
    #
    # Only customer-specific questions.
    # These require MySQL / user / device information.
    # =====================================================

    support_patterns = [

        # -------------------------------------------------
        # MY DEVICE / CAMERA
        # -------------------------------------------------

        "check my device",
        "check my camera",
        "check my sensor",

        "my device status",
        "my camera status",
        "my sensor status",

        "is my device online",
        "is my camera online",
        "is my sensor online",

        "is my device offline",
        "is my camera offline",

        "check my device status",
        "check my camera status",

        # -------------------------------------------------
        # ACCOUNT
        # -------------------------------------------------

        "check my account",
        "my account status",

        # -------------------------------------------------
        # SUBSCRIPTION
        # -------------------------------------------------

        "check my subscription",
        "my subscription",
        "my subscription status",

        "check my plan",
        "my plan",

        # -------------------------------------------------
        # FIRMWARE
        # -------------------------------------------------

        "check my firmware",
        "my firmware",
        "what is my firmware",

        # -------------------------------------------------
        # SETTINGS
        # -------------------------------------------------

        "check my settings",
        "my settings",

        # -------------------------------------------------
        # EVENTS
        # -------------------------------------------------

        "check my event",
        "check my events",

        "my latest event",
        "my latest events",

        "latest event on my device",
        "latest event on my camera",

        # -------------------------------------------------
        # ROLLOVER
        # -------------------------------------------------

        "did my rollover happen",
        "did rollover happen",

        "check my rollover",
        "Rollover event issue",
        "rollover event issue",
        "rollover",


        # NEW - customer-specific rollover questions
        "my rollover",
        "my roll over",

        "why is my rollover not working",
        "why is my roll over not working",

        "why isn't my rollover working",
        "why isn't my roll over working",

        "why was my rollover not working",
        "why was my roll over not working",

        "why didn't my rollover happen",
        "why did my rollover not happen",

        "why did my rollover fail",

        "my rollover event",
        "rollover event on my device",

        # -------------------------------------------------
        # CUSTOMER-SPECIFIC STATUS
        # -------------------------------------------------

        "check my status",
        "check my device status",
        "check my camera status"

    ]


    # =====================================================
    # DETECT SUPPORT
    # =====================================================

    for pattern in support_patterns:

        if pattern in question:

            print()
            print(">>> SUPPORT DETECTED")
            print(">>> Pattern :", pattern)
            print(">>> Route   : support")
            print(">>> Intent  :", pattern)

            return {
                **state,
                "route": "support",
                "intent": pattern
            }


    # =====================================================
    # RAG
    #
    # Generic IoT knowledge, documentation,
    # troubleshooting and how-to questions.
    # =====================================================

    rag_patterns = [

                # -------------------------------------------------
        # CHATBOT MENU OPTIONS — ROUTE TO RAG
        # -------------------------------------------------

        # Main menu
        "product information",
        "device troubleshooting",
        "hubbleclub app questions",
        "hubbleclub app questions and troubleshooting",

        # Product categories
        "ai-powered monitors",
        "smart video monitors",
        "smart soothers",
        "smart soothers & audio monitors",
        "movement trackers",
        "health & wellness devices",
        "roo - prenatal device",

        # Device troubleshooting options
        "device not powering on",
        "device not connecting to wi-fi",
        "camera offline or disconnected",
        "video/live stream not working",
        "live stream not working",
        "night vision issue",
        "motion detection false alert",
        "sound/audio issue",
        "notifications/alerts not working",
        "device setup/pairing issue",
        "firmware update issue",
        "other device issue",

        # App troubleshooting options
        "cannot log in",
        "forgot/reset password",
        "app crashing",
        "cannot add/pair a device",
        "live video not loading",
        "notifications not received",
        "subscription/membership question",
        "account/profile update",
        "app permissions",
        "app update issue",
        "other app issue",

        # -------------------------------------------------
        # CAMERA
        # -------------------------------------------------

        "camera",
        "camera issue",
        "camera problem",
        "camera not working",
        "camera stopped working",
        "camera troubleshooting",

        # -------------------------------------------------
        # MOTION
        # -------------------------------------------------

        "motion",
        "motion detection",
        "motion alert",
        "false alert",
        "false motion",
        "motion issue",
        "motion problem",

        # -------------------------------------------------
        # ROLLOVER
        # -------------------------------------------------


        # -------------------------------------------------
        # FIRMWARE
        # -------------------------------------------------

        "firmware",
        "firmware update",
        "update firmware",

        # -------------------------------------------------
        # SUBSCRIPTION
        # -------------------------------------------------

        "subscription",
        "subscription plan",
        "subscription plans",

        # -------------------------------------------------
        # DEVICE
        # -------------------------------------------------

        "device setup",
        "device installation",
        "device issue",
        "device problem",

        # -------------------------------------------------
        # SENSOR
        # -------------------------------------------------

        "sensor",
        "sensors",
        "sensor issue",
        "sensor problem",

        # -------------------------------------------------
        # NOTIFICATION
        # -------------------------------------------------

        "notification",
        "notifications",
        "notification issue",

        # -------------------------------------------------
        # BATTERY
        # -------------------------------------------------

        "battery",
        "battery issue",
        "battery problem",

        # -------------------------------------------------
        # SETUP / INSTALLATION
        # -------------------------------------------------

        "installation",
        "setup",

        # -------------------------------------------------
        # GENERIC KNOWLEDGE / HOW-TO
        # -------------------------------------------------

        "how do i",
        "how do you",
        "how to",

        "what is",
        "what are",
        "what does",
        "what does it mean",

        "how does",
        "how can i",

        "explain",
        "guide",
        "instructions",
        "steps",

        "troubleshoot",
        "troubleshooting",

        "help me understand"

    ]


    # =====================================================
    # DETECT RAG
    # =====================================================

    for pattern in rag_patterns:

        if pattern in question:

            print()
            print(">>> RAG DETECTED")
            print(">>> Pattern :", pattern)
            print(">>> Route   : rag")
            print(">>> Intent  :", pattern)

            return {
                **state,
                "route": "rag",
                "intent": pattern
            }


    # =====================================================
    # GENERAL CHAT
    # =====================================================

    print()
    print(">>> GENERAL CHAT")
    print(">>> Route : general")

    return {
        **state,
        "route": "general",
        "intent": "general"
    }