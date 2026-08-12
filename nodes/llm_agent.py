import time
from llm.ollama_client import llm


def llm_agent(state):

    prompt = f"""
You are an experienced IoT Customer Support Engineer.

Rewrite the following support report into a professional,
friendly, and easy-to-understand customer response.

Instructions:
- Start directly with a greeting (e.g., "Dear Raghavendra,").
- Do NOT write phrases like:
  - "Here's a rewritten response"
  - "Based on the report"
  - "According to the report"
- Do not invent or assume information.
- Use only the information provided.
- Keep the response concise and professional.
- End by politely asking for additional details only if the report indicates missing information.

Support Report:

{state["answer"]}
"""

    start = time.time()

    response = llm.invoke(prompt)

    print(f"LLM Time: {time.time() - start:.2f} sec")

    return {
        **state,
        "answer": response.content.strip()
    }