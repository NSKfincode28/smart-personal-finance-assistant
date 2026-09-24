import os
from pathlib import Path

from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver

from memory_store import ProfileMemoryStore
from tools import build_agent_tools


# ---------------------------------------------------------
# PROJECT SETTINGS
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent

MEMORY_PATH = (
    PROJECT_ROOT
    / "data"
    / "profile_memory.json"
)


# ---------------------------------------------------------
# AGENT INSTRUCTIONS
# ---------------------------------------------------------

SYSTEM_PROMPT = """
You are a Smart Personal Finance Assistant.

Your job is to help users understand simple personal
expense information and provide basic budgeting guidance.

IMPORTANT RULES:

1. Use expense_calculator for exact arithmetic.

2. Use budget_guidance_lookup when the user asks for
   budgeting guidance about an expense category.

3. Use remember_preference when the user explicitly asks
   you to remember a spending preference.

4. Use read_preferences when the user's previous preference
   should influence a recommendation.

5. Never invent missing expense amounts.

6. Never invent budgeting guidance that is not available
   in the local knowledge source.

7. If a tool returns ERROR or NO_DATA, clearly explain
   the problem to the user.

8. Keep responses simple and easy to understand.

9. Explain briefly when you used a tool.

This is a teaching prototype.
Do not claim that you have access to bank accounts,
live financial data or live web information.
"""


# ---------------------------------------------------------
# CREATE LLM
# ---------------------------------------------------------

def create_llm():

    model_name = os.getenv(
        "OPENAI_MODEL",
        "gpt-4o-mini"
    )

    model = ChatOpenAI(
        model=model_name,
        temperature=0.2,
        max_tokens=500
    )

    return model


# ---------------------------------------------------------
# CREATE AGENT
# ---------------------------------------------------------

def create_finance_agent():

    load_dotenv()

    if not os.getenv("OPENAI_API_KEY"):

        raise RuntimeError(
            "OPENAI_API_KEY is missing from .env"
        )

    # 1. Create the LLM
    model = create_llm()

    # 2. Create persistent memory
    profile_store = ProfileMemoryStore(
        MEMORY_PATH
    )

    # 3. Create tools
    tools = build_agent_tools(
        profile_store
    )

    # 4. Create short-term/session memory
    checkpointer = InMemorySaver()

    # 5. Create the agent
    agent = create_agent(
        model=model,
        tools=tools,
        system_prompt=SYSTEM_PROMPT,
        checkpointer=checkpointer
    )

    return agent


# ---------------------------------------------------------
# RUN AGENT
# ---------------------------------------------------------

def ask_agent(
    agent,
    question,
    thread_id="finance-session-01"
):

    result = agent.invoke(

        {
            "messages": [
                {
                    "role": "user",
                    "content": question
                }
            ]
        },

        {
            "configurable": {
                "thread_id": thread_id
            }
        }
    )

    messages = result["messages"]

    final_message = messages[-1]

    return final_message.content


# ---------------------------------------------------------
# SIMPLE TRACE
# ---------------------------------------------------------

def show_trace(agent, question):

    result = agent.invoke(

        {
            "messages": [
                {
                    "role": "user",
                    "content": question
                }
            ]
        },

        {
            "configurable": {
                "thread_id": "trace-session"
            }
        }
    )

    print("\n========== TRACE ==========")

    for message in result["messages"]:

        message_type = getattr(
            message,
            "type",
            "unknown"
        )

        if message_type == "human":

            print(
                f"\nUSER:\n{message.content}"
            )

        elif message_type == "ai":

            tool_calls = getattr(
                message,
                "tool_calls",
                []
            )

            if tool_calls:

                for call in tool_calls:

                    print(
                        "\nMODEL REQUESTED TOOL:"
                    )

                    print(
                        f"Tool: {call['name']}"
                    )

                    print(
                        f"Arguments: {call['args']}"
                    )

            else:

                print(
                    f"\nASSISTANT:\n{message.content}"
                )

        elif message_type == "tool":

            print(
                f"\nTOOL RESULT:\n{message.content}"
            )

    print(
        "\n============================"
    )


# ---------------------------------------------------------
# MAIN PROGRAM
# ---------------------------------------------------------

def main():

    print(
        "\n===================================="
    )

    print(
        " SMART PERSONAL FINANCE ASSISTANT"
    )

    print(
        "===================================="
    )

    agent = create_finance_agent()

    print(
        "\nType 'exit' to quit."
    )

    while True:

        question = input(
            "\nYou: "
        ).strip()

        if question.lower() == "exit":

            print(
                "\nGoodbye!"
            )

            break

        if not question:

            continue

        try:

            answer = ask_agent(
                agent,
                question
            )

            print(
                "\nAssistant:"
            )

            print(answer)

        except Exception as error:

            print(
                f"\nSomething went wrong: {error}"
            )


if __name__ == "__main__":
    main()
