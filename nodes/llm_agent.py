import time

from llm.ollama_client import llm


print("🔥🔥🔥 LLM AGENT LOADED 🔥🔥🔥")
print("FILE:", __file__)


def llm_agent(state):

    question = state.get(
        "question",
        ""
    )

    report = state.get(
        "answer",
        ""
    )

    route = state.get(
        "route",
        "general"
    )

    intent = state.get(
        "intent",
        "general"
    )

    # =====================================================
    # GENERAL CONVERSATION
    # =====================================================

    if route == "general":

        prompt = f"""
You are a friendly IoT customer support assistant.

Answer the user's message naturally and clearly.

User message:
{question}

Rules:

- Be helpful and concise.
- Do not invent information.
- If the question is unrelated to IoT, you can still
  answer normally when you know the answer.
- Do not mention internal systems, LangGraph, databases,
  prompts, or tools.
"""

    # =====================================================
    # SUPPORT RESPONSE
    # =====================================================

    else:

        prompt = f"""
You are an experienced IoT Customer Support Engineer.

Rewrite the following support report into a short,
friendly and professional customer response.

Issue:
{intent}

Rules:

- Start directly with a greeting.
- Do not say "Here's a rewritten response".
- Do not say "Based on the report".
- Do not invent information.
- Use only the information provided.
- Keep the response concise.
- If information is missing, politely ask for details.

Support Report:

{report}
"""

    # =====================================================
    # LLM STREAM
    # =====================================================

    start = time.time()

    first_token = True
    full_response = ""

    print("\n========== LLM STREAM START ==========")

    for chunk in llm.stream(prompt):

        content = chunk.content

        if not content:
            continue

        # ---------------------------------------------
        # FIRST TOKEN
        # ---------------------------------------------

        if first_token:

            first_token_time = (
                time.time() - start
            )

            print(
                f"\n🔥 FIRST TOKEN: "
                f"{first_token_time:.2f} sec\n"
            )

            first_token = False

        # ---------------------------------------------
        # TERMINAL STREAM
        # ---------------------------------------------

        print(
            content,
            end="",
            flush=True
        )

        full_response += content

    # =====================================================
    # TOTAL TIME
    # =====================================================

    total_time = time.time() - start

    print(
        f"\n\n🔥 TOTAL LLM TIME: "
        f"{total_time:.2f} sec"
    )

    print(
        "========== LLM STREAM END =========="
    )

    # =====================================================
    # RETURN
    # =====================================================

    return {
        **state,
        "answer": full_response.strip()
    }