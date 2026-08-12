def ask_username(state):

    print(">>> ask_username")
    print(state)

    # Username/email already received
    if state.get("username"):
        return {
            "answer": ""
        }

    # Get the issue from state
    issue = state.get("question", "support")

    return {
        "answer": (
            f"Sure! I can help you investigate the {issue} issue.\n\n"
            "Before I proceed, please enter your username or email address."
        )
    }

