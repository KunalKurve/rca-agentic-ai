import json
from difflib import SequenceMatcher
from langgraph_flow import flow

def similarity(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def evaluate_case(query, expected_root_cause):
    result = flow.invoke({"input": query})
    predicted = result["report"]["causal_chain"].get("root_cause", "")

    score = similarity(expected_root_cause, predicted)

    return {
        "query": query,
        "expected_root_cause": expected_root_cause,
        "predicted_root_cause": predicted,
        "score": round(score, 2)
    }

def main():
    with open("data/ground_truth.json", "r") as f:
        test_cases = json.load(f)

    results = []
    for case in test_cases:
        results.append(evaluate_case(case["query"], case["expected_root_cause"]))

    print("\nEvaluation Results:\n")
    for row in results:
        print(row)

if __name__ == "__main__":
    main()