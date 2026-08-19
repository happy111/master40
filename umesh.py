import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path


APPROVAL_FILE = Path("deployment/approval.json")


def create_approval(approved: bool, approver: str, commit_sha: str):
    if not approved:
        print("Ontology was NOT approved.")
        return

    APPROVAL_FILE.parent.mkdir(parents=True, exist_ok=True)

    approval = {
        "status": "approved",
        "approvedBy": approver,
        "approvedAt": datetime.now(timezone.utc).isoformat(),
        "commitSha": commit_sha,
    }

    with APPROVAL_FILE.open("w", encoding="utf-8") as file:
        json.dump(approval, file, indent=2)

    print("=" * 60)
    print("ONTOLOGY APPROVAL")
    print("=" * 60)
    print(json.dumps(approval, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--approve",
        action="store_true",
        help="Approve the ontology"
    )

    parser.add_argument(
        "--approver",
        required=True
    )

    parser.add_argument(
        "--commit",
        default=os.getenv("GIT_COMMIT", "LOCAL-DEMO-COMMIT")
    )

    args = parser.parse_args()

    create_approval(
        approved=args.approve,
        approver=args.approver,
        commit_sha=args.commit,
    )
