def router(state):

    question = state["question"].lower()

    support_words = [

        "rollover",
        "flip",
        "cry",
        "sleep",
        "firmware",
        "subscription",
        "plan",
        "camera",
        "offline"

    ]

    if any(word in question for word in support_words):

        return {
            "route":"support"
        }

    return {
        "route":"rag"
    }