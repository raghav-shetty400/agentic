from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    Response,
    stream_with_context
)

from graph.builder import graph
from llm.ollama_client import llm

import time


app = Flask(
    __name__,
    template_folder="frontend/templates"
)


# =====================================================
# HOME
# =====================================================

@app.route("/")
def home():

    return render_template("index.html")


# =====================================================
# CHAT
# =====================================================

@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()

    message = data.get("message", "")

    result = graph.invoke({

        "question": message,
        "username": "",
        "answer": "",
        "route": ""

    })

    return jsonify({

        "reply": result.get("answer", "")

    })


# =====================================================
# SEARCH USER
# =====================================================

@app.route("/search-user", methods=["POST"])
def search_user():

    data = request.get_json()

    username = data.get("username", "")
    issue = data.get("issue", "rollover")

    print()
    print("========================================")
    print("SEARCH USER")
    print("Username :", username)
    print("Issue    :", issue)
    print("========================================")


    # -------------------------------------------------
    # RUN LANGGRAPH
    # -------------------------------------------------

    result = graph.invoke({

        "question": issue,
        "username": username,
        "answer": "",
        "route": "support"

    })


    print("========== SUPPORT REPORT ==========")
    print(result)
    print("====================================")


    # -------------------------------------------------
    # GET SUPPORT REPORT
    # -------------------------------------------------

    report = result.get(
        "answer",
        "Unable to generate support report."
    )


    # -------------------------------------------------
    # LLM PROMPT
    # -------------------------------------------------

    prompt = f"""
You are an experienced IoT Customer Support Engineer.

Rewrite the following support report into a short,
friendly and professional customer response.

Rules:

- Start directly with a greeting.
- Do NOT say "Here's a rewritten response".
- Do NOT say "Based on the report".
- Do NOT invent information.
- Use only the information provided.
- Keep the response concise.
- Do not ask unnecessary questions.

Support Report:

{report}
"""


    # -------------------------------------------------
    # STREAM LLM TO BROWSER
    # -------------------------------------------------

    def generate():

        start = time.time()

        first_token = True

        print()
        print("========== LLM STREAM START ==========")


        for chunk in llm.stream(prompt):

            content = chunk.content

            if not content:
                continue


            # -----------------------------------------
            # FIRST TOKEN
            # -----------------------------------------

            if first_token:

                first_token_time = time.time() - start

                print(
                    f"\n🔥 FIRST TOKEN: "
                    f"{first_token_time:.2f} sec\n"
                )

                first_token = False


            # -----------------------------------------
            # TERMINAL
            # -----------------------------------------

            print(
                content,
                end="",
                flush=True
            )


            # -----------------------------------------
            # BROWSER
            # -----------------------------------------

            yield content


        total_time = time.time() - start

        print()

        print(
            f"🔥 TOTAL LLM TIME: "
            f"{total_time:.2f} sec"
        )

        print("========== LLM STREAM END ==========")


    return Response(

        stream_with_context(generate()),

        mimetype="text/plain",

        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no"
        }

    )


# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":

    app.run(
        debug=True,
        threaded=True
    )