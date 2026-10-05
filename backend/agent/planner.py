from typing import List

from backend.agent.state import AgentState

# Default workflow for product-analysis tasks
PRODUCT_ANALYSIS_PLAN = [
    "understand_requirements",
    "inspect_product",
    "analyze_ingredients",
    "evaluate_product",
    "search_alternatives",
    "compare_alternatives",
    "request_human_approval",
    "verify_result",
    "complete_task",
]


def create_plan(goal: str) -> List[str]:
    """
    Create an initial execution plan based on the user's goal.

    The first version uses deterministic rules.
    We will later replace/augment this with an LLM-based planner.
    """

    goal_lower = goal.lower()

    plan = []

    # Step 1: Understand the user's requirements
    plan.append("understand_requirements")

    # Product/food analysis
    product_keywords = [
        "product",
        "food",
        "ingredient",
        "ingredients",
        "snack",
        "protein",
        "bar",
        "label",
    ]

    is_product_task = any(
        keyword in goal_lower
        for keyword in product_keywords
    )

    if is_product_task:

        plan.extend([
            "inspect_product",
            "analyze_ingredients",
            "evaluate_product",
        ])

        # If the user is asking for alternatives/recommendations, search the product environment.
        alternative_keywords = [
            "alternative",
            "alternatives",
            "recommend",
            "recommendation",
            "better",
            "replace",
            "replacement",
            "instead",
            "find",
        ]

        wants_alternative = any(
            keyword in goal_lower
            for keyword in alternative_keywords
        )

        if wants_alternative:
            plan.extend([
                "search_alternatives",
                "compare_alternatives",
            ])

    # Human approval
    plan.append("request_human_approval")

    # Verification and completion
    plan.extend([
        "verify_result",
        "complete_task",
    ])

    return plan


def initialize_plan(state: AgentState) -> AgentState:
    """
    Generate and attach an execution plan to AgentState.
    """

    state.plan = create_plan(state.goal)

    state.current_step = 0

    state.status = "planned"

    return state