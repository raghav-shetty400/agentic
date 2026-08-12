def log_node(state):
    print("===== LOG =====")
    print(f"Username : {state['username']}")
    print(f"Question : {state['question']}")
    print(f"Answer   : {state['answer']}")
    print("================")

    return state