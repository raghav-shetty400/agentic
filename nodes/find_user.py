from tools.user_tool import get_user

def find_user(state):

    username = state["username"]

    user = get_user(username)

    if user is None:
        return {
            "answer": "Username not found."
        }

    return {
        "user": user
    }