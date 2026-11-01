from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    session,
    Response,
    stream_with_context
)

from graph.builder import graph
from llm.ollama_client import llm

import time


# =====================================================
# FLASK APP
# =====================================================

print("\n" + "=" * 80)
print("                    APPLICATION STARTING")
print("=" * 80)

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

    # Start a fresh conversation
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
        # DEBUG
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
        # USER ENTERED USERNAME / EMAIL
        # =================================================

        if session.get(
            "waiting_for_username",
            False
        ):

            username = message

            pending_issue = session.get(
                "pending_issue",
                ""
            ).strip()


            print()
            print("========== USERNAME FLOW ==========")
            print("Username :", username)
            print("Issue    :", pending_issue)
            print("===================================")


            # =================================================
            # VALIDATE PENDING ISSUE
            # =================================================

            if not pending_issue:

                print()
                print("ERROR: pending_issue is EMPTY")

                session.clear()

                return jsonify({

                    "reply":
                    "I lost the issue information. "
                    "Please select the issue again."

                }), 400


            # =================================================
            # CALL SUPPORT GRAPH
            # =================================================

            print()
            print("========== CALLING SUPPORT GRAPH ==========")
            print("Question :", pending_issue)
            print("Username :", username)
            print("Route    : support")
            print("Intent   :", pending_issue)
            print("===========================================")


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
            # GET SUPPORT REPORT
            # =================================================

            support_report = result.get(
                "answer",
                ""
            )


            # =================================================
            # SUPPORT GRAPH FAILED
            # =================================================

            if not support_report:

                print()
                print("WARNING: Support graph returned EMPTY answer")
                print("Route  :", result.get("route"))
                print("Intent :", result.get("intent"))

                session.clear()

                return jsonify({

                    "reply":
                    "I couldn't generate a support response."

                }), 500


            # =================================================
            # SUPPORT SUCCESS
            # =================================================

            print()
            print("========== SUPPORT SUCCESS ==========")
            print("Answer :")
            print(support_report)
            print("======================================")


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
            # LLM PROMPT
            # =================================================

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
- Clearly explain the customer's issue.
- Clearly explain the current rollover status.
- Do not ask unnecessary questions.

Support Report:

{support_report}
"""


            # =================================================
            # STREAM LLM
            # =================================================

            def generate():

                start = time.time()

                first_token = True

                print()
                print("========== LLM STREAM START ==========")


                try:

                    for chunk in llm.stream(prompt):

                        content = getattr(
                            chunk,
                            "content",
                            ""
                        )


                        if not content:

                            continue


                        # =====================================
                        # FIRST TOKEN
                        # =====================================

                        if first_token:

                            first_token_time = (
                                time.time() - start
                            )

                            print(
                                f"\n🔥 FIRST TOKEN: "
                                f"{first_token_time:.2f} sec\n"
                            )

                            first_token = False


                        # =====================================
                        # TERMINAL
                        # =====================================

                        print(
                            content,
                            end="",
                            flush=True
                        )


                        # =====================================
                        # SEND TO BROWSER
                        # =====================================

                        yield content


                except Exception as e:

                    print()
                    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    print("LLM STREAM ERROR")
                    print("TYPE :", type(e).__name__)
                    print("ERROR:", str(e))
                    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

                    yield (
                        "\nSorry, I couldn't generate "
                        "the AI response."
                    )


                total_time = (
                    time.time() - start
                )


                print()
                print(
                    f"🔥 TOTAL LLM TIME: "
                    f"{total_time:.2f} sec"
                )

                print(
                    "========== LLM STREAM END =========="
                )


            # =================================================
            # RETURN STREAM
            # =================================================

            return Response(

                stream_with_context(
                    generate()
                ),

                mimetype="text/plain",

                headers={

                    "Cache-Control":
                    "no-cache",

                    "X-Accel-Buffering":
                    "no"

                }

            )


        # =================================================
        # STEP 2
        # NORMAL CHAT
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
        # READ RESULT
        # =================================================

        route = result.get(
            "route",
            "general"
        )

        intent = result.get(
            "intent",
            ""
        )

        answer = result.get(
            "answer",
            ""
        )

        context = result.get(
            "context",
            ""
        )


        print()
        print("========== ROUTING RESULT ==========")
        print("Route   :", route)
        print("Intent  :", intent)
        print("Answer  :", answer)
        print("Context :", len(context))
        print("====================================")


        # =================================================
        # SUPPORT DETECTED
        # =================================================

        if route == "support":

            print()
            print(">>> SUPPORT ISSUE DETECTED")
            print(">>> Original :", message)
            print(">>> Intent   :", intent)


            # =================================================
            # IMPORTANT
            #
            # Prefer router intent.
            # If router didn't provide one,
            # preserve original user message.
            # =================================================

            pending_issue = (
                intent.strip()
                if isinstance(intent, str)
                else ""
            )


            if not pending_issue:

                pending_issue = message


            print()
            print("========== SAVING SUPPORT ISSUE ==========")
            print("Original message :", message)
            print("Router intent    :", intent)
            print("Pending issue    :", pending_issue)
            print("==========================================")


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
            # ASK USERNAME
            # =================================================

            return jsonify({

                "reply":
                "Sure! I can help you investigate "
                f"the {pending_issue} issue.\n\n"
                "Before I proceed, please enter "
                "your username or email address."

            })


        # =================================================
        # RAG
        # =================================================

        if route == "rag":

            print()
            print(">>> RAG QUESTION DETECTED")
            print(">>> Question :", message)
            print(">>> Intent   :", intent)
            print(">>> Context length :", len(context))


            # -------------------------------------------------
            # RAG answer already generated by graph
            # -------------------------------------------------

            if answer:

                print()
                print(">>> RAG ANSWER FOUND")

                return jsonify({
                    "reply": answer
                })


         # =================================================
        # RAG
        # =================================================

        if route == "rag":

            print()
            print(">>> RAG QUESTION DETECTED")
            print(">>> Question :", message)
            print(">>> Intent   :", intent)
            print(">>> Context length :", len(context))


            # -------------------------------------------------
            # RAG CONTEXT FOUND
            # -------------------------------------------------

            if context and context.strip():

                print()
                print(">>> RAG CONTEXT FOUND")


                # =================================================
                # OLD CODE - RAG WITH LLM (TEMPORARILY DISABLED)
                # =================================================

                """
                print(">>> Generating answer using LLM...")

                rag_prompt = f\"\"\"
You are an IoT customer support knowledge assistant.

Answer the user's question using ONLY the
knowledge provided below.

Rules:

- Do not invent information.
- If the knowledge does not contain the answer,
  clearly say that the information is not available.
- Give a clear and helpful answer.
- Keep it concise and easy to understand.

User Question:

{message}

Knowledge:

{context}
\"\"\"


                def generate_rag():

                    start = time.time()

                    first_token = True

                    print()
                    print("========== RAG LLM STREAM START ==========")

                    try:

                        for chunk in llm.stream(rag_prompt):

                            content = getattr(
                                chunk,
                                "content",
                                ""
                            )

                            if not content:
                                continue

                            if first_token:

                                first_token_time = (
                                    time.time() - start
                                )

                                print(
                                    f"\\n🔥 RAG FIRST TOKEN: "
                                    f"{first_token_time:.2f} sec\\n"
                                )

                                first_token = False

                            print(
                                content,
                                end="",
                                flush=True
                            )

                            yield content

                    except Exception as e:

                        print()
                        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                        print("RAG LLM STREAM ERROR")
                        print("TYPE :", type(e).__name__)
                        print("ERROR:", str(e))
                        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

                        yield (
                            "\\nSorry, I couldn't generate "
                            "the RAG response."
                        )

                    total_time = (
                        time.time() - start
                    )

                    print()
                    print(
                        f"🔥 TOTAL RAG LLM TIME: "
                        f"{total_time:.2f} sec"
                    )

                    print(
                        "========== RAG LLM STREAM END =========="
                    )


                return Response(
                    stream_with_context(
                        generate_rag()
                    ),
                    mimetype="text/plain",
                    headers={
                        "Cache-Control": "no-cache",
                        "X-Accel-Buffering": "no"
                    }
                )

             """


                # =================================================
                # NEW CODE - RAG WITHOUT LLM
                # =================================================


        # =================================================
        # RAG - STREAMING WITHOUT LLM
        # =================================================

        if route == "rag":

            print()
            print(">>> RAG QUESTION DETECTED")
            print(">>> Question :", message)
            print(">>> Intent   :", intent)
            print(">>> Context length :", len(context))

            if context and context.strip():

                print()
                print(">>> RAG CONTEXT FOUND")

                def generate_rag():

                    start = time.time()

                    print()
                    print("========== RAG WITHOUT LLM STREAM START ==========")

                    answer = (
                        "Here is the relevant information "
                        "from our knowledge base:\n\n"
                        + context.strip()
                    )

                    chunk_size = 40

                    for i in range(0, len(answer), chunk_size):

                        chunk = answer[i:i + chunk_size]

                        print(chunk, end="", flush=True)

                        yield chunk

                        time.sleep(0.02)

                    total_time = time.time() - start

                    print()
                    print(
                        f"🔥 RAG STREAM TOTAL TIME: "
                        f"{total_time:.4f} sec"
                    )

                    print("========== RAG WITHOUT LLM STREAM END ==========")

                return Response(
                    stream_with_context(generate_rag()),
                    mimetype="text/plain",
                    headers={
                        "Cache-Control": "no-cache",
                        "X-Accel-Buffering": "no"
                    }
                )
            
        # =================================================
        # RAG CONTEXT IS EMPTY"
        # =================================================
            

            else:

                print()
                print("WARNING: RAG CONTEXT IS EMPTY")

                return jsonify({
                    "reply": (
                        "Sorry, I couldn't find relevant "
                        "information in our knowledge base."
                    )
                })

            # -------------------------------------------------
            # RAG returned nothing
            # -------------------------------------------------

            print()
            print("WARNING: RAG returned EMPTY answer")
            print("WARNING: RAG context is also EMPTY")


            return jsonify({

                "reply":
                "I couldn't find relevant information "
                "in the knowledge base."

            })


        

        # =================================================
        # GENERAL CHAT - STREAMING
        # =================================================

        if route == "general":

            print()
            print(">>> GENERAL CHAT STREAMING")

            # Use an existing answer if available
            if answer:
                return jsonify({
                    "reply": answer
                })

            print(">>> Generating response using Ollama...")

            general_prompt = f"""
You are a friendly, helpful conversational AI assistant.

User message:
{message}

Instructions:
- Respond directly to the user's message.
- Handle greetings, small talk, thanks, and general questions naturally.
- Avoid repeating the same generic response.
- Ask follow-up questions when they are useful.
- Keep answers clear and concise.
- Never invent customer, account, or device information.
- Do not claim to have personal experiences or emotions.
- Technical questions about IoT knowledge belong to RAG.
- Requests to check a user's actual device or account belong to Support.

Respond naturally to the user's message.
"""

            def generate_general_response():

                try:
                    for chunk in llm.stream(general_prompt):

                        content = getattr(
                            chunk,
                            "content",
                            ""
                        )

                        if content:
                            print(
                                ">>> GENERAL CHUNK:",
                                repr(content)
                            )

                            yield content

                except Exception as e:
                    print(
                        ">>> GENERAL STREAM ERROR:",
                        str(e)
                    )

                    yield "\nSorry, I couldn't complete the response."

            return Response(
                stream_with_context(
                    generate_general_response()
                ),
                content_type="text/plain; charset=utf-8"
            )

        # =================================================
        # UNKNOWN ROUTE
        # =================================================

        print()
        print("WARNING: UNKNOWN ROUTE")


        # =================================================
        # UNKNOWN ROUTE
        # =================================================

        print()
        print("WARNING: UNKNOWN ROUTE")
        print("Route :", route)


        return jsonify({

            "reply":
            "I'm not sure how to handle that request."

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