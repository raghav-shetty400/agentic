import time
from llm.ollama_client import llm


def llm_agent(state):

    prompt = f"""
You are an IoT customer support engineer.

Rewrite this support report as a short, friendly
customer response.

Rules:
- Start with "Dear Raghavendra,"
- Do not invent information.
- Use only the report.
- Keep it concise.
- Do not say "Here's a rewritten response".

Report:

{state["answer"]}
"""

    start = time.time()
    first_token = True
    full_response = ""

    print("\n========== LLM STREAM START ==========")

    for chunk in llm.stream(prompt):

        if first_token:
            print(
                f"\nFIRST TOKEN: {time.time() - start:.2f} sec\n"
            )
            first_token = False

        content = chunk.content

        if content:
            print(content, end="", flush=True)
            full_response += content

    print(
        f"\nLLM TOTAL: {time.time() - start:.2f} sec"
    )

    print("========== LLM STREAM END ==========")

    return {
        **state,
        "answer": full_response.strip()
    }