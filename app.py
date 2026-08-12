from flask import Flask, render_template, request, jsonify, Response, stream_with_context

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

        "reply": result["answer"]

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


    print("========== SEARCH USER RESULT ==========")
    print(result)
    print("========================================")


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

Rewrite the following support report into a professional,
friendly, and easy-to-understand customer response.

Instructions:

- Start directly with a greeting.
- Do NOT write "Here's a rewritten response".
- Do NOT write "Based on the report".
- Do NOT invent information.
- Use only the information provided.
- Keep the response concise and professional.
- If information is missing, politely ask for additional details.

Support Report:

{report}
"""


    # -------------------------------------------------
    # STREAM LLM RESPONSE
    # -------------------------------------------------

    def generate():

        start = time.time()

        print()
        print("========== LLM STREAM START ==========")


        for chunk in llm.stream(prompt):

            if chunk.content:

                # Show generated text in Flask terminal

                print(
                    chunk.content,
                    end="",
                    flush=True
                )


                # Send generated text immediately
                # to the browser

                yield chunk.content


        print()

        print(
            f"LLM Time: "
            f"{time.time() - start:.2f} sec"
        )

        print("========== LLM STREAM END ==========")


    return Response(

        stream_with_context(generate()),

        mimetype="text/plain"

    )


# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":

    app.run(
        debug=True,
        threaded=True
    )
