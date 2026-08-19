def identify_approver(ontology_type):
    approvers = {
        "commercial": "reviewer@example.com",
        "medical": "medical-reviewer@example.com"
    }

    return approvers.get(ontology_type)


if __name__ == "__main__":
    reviewer = identify_approver("commercial")
    print(f"Approver: {reviewer}")
