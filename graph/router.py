def router(state):

    question = state.get("question", "").lower().strip()

    print("\n========== ROUTER ==========")
    print("Question:", question)

    # =================================================
    # ROLLOVER
    # =================================================

    rollover_keywords = [
        "rollover",
        "roll over",
        "roll-over"
    ]

    if any(keyword in question for keyword in rollover_keywords):

        # If the user is actually reporting a problem,
        # send it for verification.
        problem_keywords = [
            "issue",
            "problem",
            "not working",
            "doesn't work",
            "not triggering",
            "not detected",
            "failed",
            "failure",
            "error",
            "missing",
            "wrong",
            "didn't happen",
            "not happening"
        ]

        if any(keyword in question for keyword in problem_keywords):

            print("Intent: rollover")
            print("Route: support")

            return {
                **state,
                "intent": "rollover",
                "route": "support"
            }

        # General question about rollover
        print("Intent: rollover")
        print("Route: general")

        return {
            **state,
            "intent": "rollover",
            "route": "general"
        }

    # =================================================
    # OTHER SUPPORT ISSUES
    # =================================================

    support_keywords = [
        "camera issue",
        "camera problem",
        "motion alert",
        "motion detection",
        "firmware issue",
        "subscription issue",
        "device issue",
        "device not working",
        "alert problem"
    ]

    if any(keyword in question for keyword in support_keywords):

        print("Intent: support")
        print("Route: support")

        return {
            **state,
            "intent": "support",
            "route": "support"
        }

    # =================================================
    # EVERYTHING ELSE
    # =================================================

    print("Intent: general")
    print("Route: general")

    return {
        **state,
        "intent": "general",
        "route": "general"
    }