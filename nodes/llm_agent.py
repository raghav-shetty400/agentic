import time

from llm.ollama_client import llm


print("🔥🔥🔥 NEW LLM AGENT LOADED 🔥🔥🔥")
print("🔥 FILE:", __file__)


def llm_agent(state):

    prompt = f"""
You are an IoT customer support engineer.

Rewrite this support report into a short, friendly,
professional customer response.

Rules:

- Start directly with a greeting.
- Do not say "Here's a rewritten response".
- Do not invent information.
- Use only the information in the report.
- Keep the response concise.

Support Report:

{state["answer"]}
"""

    start = time.time()

    first_token = True
    full_response = ""

    print("\n========== NEW LLM STREAM ==========")

    for chunk in llm.stream(prompt):

        content = chunk.content

        if not content:
            continue

        # FIRST TOKEN
        if first_token:

            first_token_time = time.time() - start

            print(
                f"\n\n🔥🔥🔥 FIRST TOKEN: "
                f"{first_token_time:.2f} seconds 🔥🔥🔥\n"
            )

            first_token = False

        # STREAM OUTPUT
        print(
            content,
            end="",
            flush=True
        )

        full_response += content

    total_time = time.time() - start

    print(
        f"\n\n🔥🔥🔥 TOTAL LLM TIME: "
        f"{total_time:.2f} seconds 🔥🔥🔥"
    )

    print("\n========== NEW LLM STREAM END ==========")

    return {
        **state,
        "answer": full_response.strip()
    }