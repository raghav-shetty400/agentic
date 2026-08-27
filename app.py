from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    session
)

from graph.builder import graph


# =====================================================
# FLASK APP
# =====================================================

app = Flask(
    __name__,
    template_folder="frontend/templates"
)

app.secret_key = "agentic-chatbot-secret-key"


# =====================================================
# HOME
# =====================================================

@app.route("/")
def home():

    # Start fresh conversation
    session.clear()

    return render_template("index.html")


# =====================================================
# CHAT
# =====================================================

@app.route("/chat", methods=["POST"])
def chat():

    try:

        data = request.get_json() or {}

        message = data.get(
            "message",
            ""
        ).strip()


        # =================================================
        # DEBUG - EVERY REQUEST
        # =================================================

        print()
        print("========================================")
        print("CHAT REQUEST")
        print("Message :", message)
        print("Waiting :", session.get(
            "waiting_for_username",
            False
        ))
        print("Pending :", session.get(
            "pending_issue",
            ""
        ))
        print("========================================")


        # =================================================
        # EMPTY MESSAGE
        # =================================================

        if not message:

            return jsonify({
                "reply": "Please enter a message."
            })


        # =================================================
        # STEP 1
        # USER IS PROVIDING USERNAME / EMAIL
        # =================================================

        if session.get(
            "waiting_for_username",
            False
        ):

            username = message

            pending_issue = session.get(
                "pending_issue",
                ""
            )


            print()
            print("========== USERNAME FLOW ==========")
            print("Username :", username)
            print("Issue    :", pending_issue)
            print("===================================")


            # =================================================
            # CHECK PENDING ISSUE
            # =================================================

            if not pending_issue:

                print()
                print("ERROR: pending_issue is EMPTY")
                print("Cannot continue support flow.")

                session.clear()

                return jsonify({

                    "reply":
                    "I lost the issue information. "
                    "Please select the issue again."

                }), 400


            # =================================================
            # CLEAR WAITING FLAG
            # =================================================

            session["waiting_for_username"] = False


            # =================================================
            # CALL SUPPORT GRAPH
            # =================================================

            print()
            print("========== CALLING SUPPORT GRAPH ==========")

            print("Question :", pending_issue)
            print("Username :", username)
            print("Route    : support")
            print("Intent   :", pending_issue)


            result = graph.invoke({

                "question": pending_issue,

                "username": username,

                "answer": "",

                "route": "support",

                "intent": pending_issue

            })


            print()
            print("========== SUPPORT GRAPH RESULT ==========")
            print(result)
            print("===========================================")


            # =================================================
            # GET ANSWER
            # =================================================

            answer = result.get(
                "answer",
                ""
            )


            # =================================================
            # CLEAR SESSION
            # =================================================

            session.pop(
                "pending_issue",
                None
            )


            session.pop(
                "waiting_for_username",
                None
            )


            # =================================================
            # EMPTY ANSWER
            # =================================================

            if not answer:

                print()
                print(
                    "WARNING: Support graph returned "
                    "EMPTY answer"
                )

                return jsonify({

                    "reply":
                    "I couldn't generate a support response."

                })


            # =================================================
            # SUCCESS
            # =================================================

            print()
            print("========== SUPPORT SUCCESS ==========")
            print("Answer :", answer)
            print("======================================")


            return jsonify({

                "reply": answer

            })


        # =================================================
        # STEP 2
        # NORMAL CHAT / FIRST USER MESSAGE
        # =================================================

        print()
        print("========== NORMAL CHAT ==========")
        print("Question :", message)
        print("=================================")


        # =================================================
        # CALL GRAPH
        # =================================================

        result = graph.invoke({

            "question": message,

            "username": "",

            "answer": "",

            "route": "",

            "intent": ""

        })


        print()
        print("========== GRAPH RESULT ==========")
        print(result)
        print("==================================")


        # =================================================
        # READ GRAPH RESULT
        # =================================================

        route = result.get(
            "route",
            "rag"
        )


        intent = result.get(
            "intent",
            ""
        )


        answer = result.get(
            "answer",
            ""
        )


        print()
        print("========== ROUTING RESULT ==========")
        print("Route  :", route)
        print("Intent :", intent)
        print("Answer :", answer)
        print("====================================")


        # =================================================
        # SUPPORT ISSUE
        # =================================================

        if route == "support":

            print()
            print(">>> SUPPORT ISSUE DETECTED")


            # =================================================
            # IMPORTANT
            #
            # If router does not return intent,
            # use the ORIGINAL USER MESSAGE.
            # =================================================

            pending_issue = intent.strip()


            if not pending_issue:

                pending_issue = message


            print()
            print("========== SUPPORT ISSUE ==========")
            print("Original message :", message)
            print("Graph intent     :", intent)
            print("Pending issue    :", pending_issue)
            print("===================================")


            # =================================================
            # SAVE SESSION
            # =================================================

            session["pending_issue"] = pending_issue

            session["waiting_for_username"] = True


            print()
            print("========== SESSION ==========")
            print(
                "Waiting :",
                session.get(
                    "waiting_for_username"
                )
            )
            print(
                "Pending :",
                session.get(
                    "pending_issue"
                )
            )
            print("=============================")


            # =================================================
            # ASK USERNAME / EMAIL
            # =================================================

            return jsonify({

                "reply":
                "Sure! I can help you investigate "
                f"the {pending_issue} issue.\n\n"
                "Before I proceed, please enter "
                "your username or email address."

            })


        # =================================================
        # GENERAL / RAG CHAT
        # =================================================

        print()
        print(">>> GENERAL CHAT")


        # =================================================
        # IF GRAPH ALREADY GENERATED ANSWER
        # =================================================

        if answer:

            return jsonify({

                "reply": answer

            })


        # =================================================
        # NO ANSWER
        # =================================================

        print()
        print("WARNING: General graph returned empty answer")


        return jsonify({

            "reply":
            "How can I help you today?"

        })


    # =====================================================
    # ERROR HANDLING
    # =====================================================

    except Exception as e:

        print()
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("CHAT ERROR")
        print("TYPE :", type(e).__name__)
        print("ERROR:", str(e))
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")


        return jsonify({

            "reply":
            "Sorry, I couldn't process your "
            "request right now."

        }), 500


# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":

    app.run(
        debug=True,
        threaded=True
    )