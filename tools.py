import json
from pathlib import Path

from langchain_core.tools import tool


DATA_FOLDER = Path(__file__).resolve().parent / "data"


# ---------------------------------------------------------
# TOOL 1: EXPENSE CALCULATOR
# ---------------------------------------------------------

@tool
def expense_calculator(
    operation: str,
    amount: float,
    total: float = 0
) -> str:
    """
    Perform exact expense calculations.

    Use this tool for totals, percentages and differences.

    operation must be one of:
    - total
    - percentage
    - difference
    """

    try:

        if operation == "total":

            result = amount + total

            return f"Total spending is ₹{result:.2f}"

        elif operation == "percentage":

            if total <= 0:
                return "ERROR: Total spending must be greater than zero."

            result = (amount / total) * 100

            return f"{result:.2f}%"

        elif operation == "difference":

            result = abs(amount - total)

            return f"Difference is ₹{result:.2f}"

        else:

            return (
                "ERROR: Unknown operation. "
                "Use total, percentage or difference."
            )

    except (TypeError, ValueError):

        return "ERROR: Invalid numeric input."


# ---------------------------------------------------------
# TOOL 2: BUDGET GUIDANCE LOOKUP
# ---------------------------------------------------------

@tool
def budget_guidance_lookup(category: str) -> str:
    """
    Search local budgeting guidance.

    Use this tool when the user asks for guidance about
    an expense category.

    Available categories include:
    food, travel, shopping, entertainment and bills.
    """

    file_path = DATA_FOLDER / "budget_guidance.json"

    try:

        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):

        return "ERROR: Budget guidance source is unavailable."

    category = category.strip().lower()

    if category not in data:

        return (
            f"NO_DATA: No budgeting guidance was found "
            f"for category '{category}'."
        )

    item = data[category]

    return (
        f"Category: {category}\n"
        f"Description: {item['description']}\n"
        f"Guidance: {item['guidance']}"
    )


# ---------------------------------------------------------
# TOOL 3: REMEMBER PREFERENCE
# ---------------------------------------------------------

def create_memory_tools(profile_store):

    @tool
    def remember_preference(preference: str) -> str:
        """
        Save a user's spending preference permanently.

        Use this when the user explicitly asks you to remember
        a spending preference.
        """

        profile_store.save_preference(
            "spending_preference",
            preference
        )

        return f"Preference saved: {preference}"

    @tool
    def read_preferences() -> str:
        """
        Read the user's saved spending preferences.

        Use this when a recommendation should consider
        the user's previous spending preference.
        """

        preferences = profile_store.get_preferences()

        if not preferences:

            return "No saved spending preferences."

        return json.dumps(
            preferences,
            indent=2
        )

    return [
        remember_preference,
        read_preferences
    ]


# ---------------------------------------------------------
# BUILD ALL TOOLS
# ---------------------------------------------------------

def build_agent_tools(profile_store):

    memory_tools = create_memory_tools(profile_store)

    return [
        expense_calculator,
        budget_guidance_lookup,
        *memory_tools
    ]
