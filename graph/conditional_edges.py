def route_question(state):

    route = state.get("route", "general")

    print(">>> ROUTE:", route)

    if route == "support":
        return "support"

    return "general"