from tools.user_tool import get_user


def find_user(state):

    print(">>> find_user")

    username = state.get("username", "").strip()

    if not username:

        return {
            **state,
            "answer": "Please provide your username or email address."
        }

    user = get_user(username)

    if user is None:

        return {
            **state,
            "user": {},
            "answer": "Username or email address not found."
        }

    print(
        "User found:",
        user.get("name")
    )

    return {
        **state,
        "user": user,
        "answer": ""
    }