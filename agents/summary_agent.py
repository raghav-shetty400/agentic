def summary_agent(state):

    answer = state.get("answer", "")

    return {
        "answer": f"Summary: {answer}"
    }
