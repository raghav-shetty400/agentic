from mcp.client import get_weather


def tool_agent(state):

    question = state["question"]

    city = question.replace("weather", "").strip()

    result = get_weather(city)

    return {
        "answer": str(result)
    }
