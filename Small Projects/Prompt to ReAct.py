# =====================================
# ReAct: Reason + Act (One-Go Code)
# =====================================

# ----------- TOOLS -------------------
def calculator(expression):
    return eval(expression)

def search(query):
    knowledge_base = {
        "capital of france": "Paris",
        "fashionmnist classes": "10 classes"
    }
    return knowledge_base.get(query.lower(), "Not found")

# ----------- REACT AGENT --------------
def react_agent(question):
    # STEP 1: Reason
    if "calculate" in question.lower():
        thought = "This is a math problem. I should use calculator."
        action = "calculator"
        action_input = "25 * 4"

        # STEP 2: Act
        observation = calculator(action_input)

    elif "capital" in question.lower():
        thought = "This is a factual question. I should use search."
        action = "search"
        action_input = "capital of france"

        # STEP 2: Act
        observation = search(action_input)

    else:
        thought = "No suitable tool found."
        action = "none"
        observation = "N/A"

    # STEP 3: Final Answer (Structured Output)
    final_answer = {
        "tool_used": action,
        "result": observation
    }

    return {
        "Thought": thought,
        "Action": f"{action}[{action_input if action != 'none' else ''}]",
        "Observation": observation,
        "Final Answer": final_answer
    }

# ----------- RUN EXAMPLE --------------
question = "What is the capital of France?"
response = react_agent(question)

for key, value in response.items():
    print(f"{key}: {value}")
