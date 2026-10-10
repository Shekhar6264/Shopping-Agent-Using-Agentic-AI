from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.tools import tool
from langchain.agents import create_agent
from langchain.agents.middleware import PIIMiddleware

import os

# --------------------------------------------------
# 1. Load environment variables
# --------------------------------------------------

load_dotenv()

if not os.getenv("GROQ_API_KEY"):
    raise ValueError(
        "GROQ_API_KEY not found. Add it to your .env file."
    )

# --------------------------------------------------
# 2. Initialize the language model
# --------------------------------------------------

llm = ChatGroq(
    model="qwen/qwen3-32b",
    temperature=0
)

# Alternative model, if available to your Groq account:
# llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0)


# --------------------------------------------------
# 3. Customer lookup tool
# --------------------------------------------------

@tool
def get_customer_info_tool(customer_name: str) -> str:
    """
    Retrieve customer information using the customer's name.

    This is simulated data for demonstrating PII guardrails.
    In a production application, retrieve only the minimum
    necessary information from a secure database.
    """

    customers = {
        "Krishna": {
            "email": "krishna_001@abc.com",
            "credit_card": "4111-1111-1111-1111",
            "name": "Krishna",
            "loyalty_status": "Gold"
        },
        "Alice": {
            "email": "alice_002@abc.com",
            "credit_card": "5500-0000-0000-0004",
            "name": "Alice",
            "loyalty_status": "Silver"
        },
        "Bob": {
            "email": "bob2009@xyz.com",
            "credit_card": "6011-1111-1111-1117",
            "name": "Bob",
            "loyalty_status": "Bronze"
        }
    }

    customer = customers.get(customer_name.strip().title())

    if not customer:
        return "Customer not found."

    # Demonstration safeguard:
    # Never expose the complete card number unnecessarily.
    card_number = customer["credit_card"]
    last_four = card_number.replace("-", "")[-4:]

    safe_customer = {
        "name": customer["name"],
        "email": customer["email"],
        "credit_card": f"****-****-****-{last_four}",
        "loyalty_status": customer["loyalty_status"]
    }

    return str(safe_customer)


# --------------------------------------------------
# 4. Configure the agent and PII middleware
# --------------------------------------------------

agent = create_agent(
    model=llm,

    tools=[
        get_customer_info_tool
    ],

    system_prompt="""
    You are a customer service assistant.

    You can use get_customer_info_tool to retrieve customer information.

    Rules:
    1. Use the tool when a user asks for customer information.
    2. Do not invent customer details.
    3. Return only information necessary to answer the question.
    4. Never attempt to reconstruct masked or redacted information.
    5. Never expose a complete payment card number.
    6. Respect any masking or redaction applied by middleware.
    7. If a customer is not found, state that clearly.
    """,

    middleware=[
        # Mask credit card numbers in user input,
        # tool results, and AI output.
        PIIMiddleware(
            "credit_card",
            strategy="mask",
            apply_to_input=True,
            apply_to_tool_results=True,
            apply_to_output=True
        ),

        # Redact email addresses in user input,
        # tool results, and AI output.
        PIIMiddleware(
            "email",
            strategy="redact",
            apply_to_input=True,
            apply_to_tool_results=True,
            apply_to_output=True
        )
    ]
)


# --------------------------------------------------
# 5. Invoke the agent
# --------------------------------------------------

if __name__ == "__main__":

    result = agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": "Give me information about customer Krishna."
            }
        ]
    })

    print("\nCUSTOMER SERVICE AGENT")
    print("=" * 50)
    print(result["messages"][-1].content)