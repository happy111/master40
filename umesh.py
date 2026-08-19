1. POC objective
Title

Ontology Approval & Deployment Workflow – POC

Objective

The objective of this POC is to demonstrate a lightweight workflow for:

Validating an ontology using SHACL
Identifying the designated reviewer
Automatically notifying the reviewer by email
Recording reviewer approval against a specific Git commit
Generating a deployment manifest.json
Preparing the approved ontology artifacts for controlled deployment to S3

The POC follows the proposed:

Protégé → Bitbucket → Jenkins → Approval → Manifest → S3

2. What you have implemented

Your current local POC contains these steps:

1. Validate ontology
        ↓
2. Identify reviewer
        ↓
3. Send approval email
        ↓
4. Record approval
        ↓
5. Generate manifest
        ↓
6. Deploy approved artifacts to S3


3. Step-by-step documentation
Step 1 — Validate Ontology
Command

python scripts/validate_ontology.py

Purpose

This step validates the ontology and associated SHACL rules before the ontology enters the approval process.

Expected output
============================================================
ONTOLOGY VALIDATION
============================================================

Ontology: ontology/commercial-domain-model.ttl
Triple count: 14

Validation Report
Conforms: True

SHACL validation PASSED

"First, the pipeline validates the submitted ontology using SHACL. If validation fails, the pipeline stops and the ontology is not sent for approval."
4. Step 2 — Identify Reviewer
Command
python scripts/identify_approver.py commercial
Output
 umesh.samal_ext@novartis.com
The actual reviewer email should come from your configured approver mapping.

Purpose

The application determines who is responsible for reviewing the ontology based on its type/domain.

For example:
approvers:
  commercial:
    - umesh.samal_ext@novartis.com

  medical:
    - medical-reviewer@example.com

5. Step 3 — Send Approval Email

Your command:
python scripts/send_approval_email.py \
  --approver "umesh.samal_ext@novartis.com" \
  --ontology "commercial-domain-model" \
  --version "0.1.0" \
  --commit "LOCAL-DEMO-001" \
  --url "https://your-git-server/your-repository/commit/LOCAL-DEMO-001"

Purpose

The application sends an email to the designated reviewer.

The email contains:

Ontology:
commercial-domain-model

Version:
0.1.0

Git Commit:
LOCAL-DEMO-001

Review URL:
https://your-git-server/...

Output :-

============================================================
SENDING APPROVAL EMAIL
============================================================

To: umesh.samal_ext@novartis.com
Ontology: commercial-domain-model
Version: 0.1.0
Commit: LOCAL-DEMO-001
URL: https://your-git-server/...

Approval email sent successfully.

Simple explanation to manager

"Once the ontology passes validation, the POC automatically sends an approval notification to the designated reviewer. The email includes the ontology name, version, commit SHA, and review link so that the reviewer knows exactly which version needs to be reviewed."

 6. Step 4 — Record Approval

Your command:
python scripts/approval.py \
  --approve \
  --approver "umesh.samal_ext@novartis.com" \
  --commit "LOCAL-DEMO-001

Purpose

This records:

Approval status
Approver
Approval timestamp
Git commit SHA

Example:

{
  "status": "approved",
  "approvedBy": "umesh.samal_ext@novartis.com",
  "approvedAt": "2026-08-19T12:30:00+00:00",
  "commitSha": "LOCAL-DEMO-001"
}

Tell your manager

"The approval is recorded against the exact Git commit, so we can trace which ontology version was approved and by whom."


7. Step 5 — Generate Manifest
Command

python scripts/generate_manifest.py

output :-

Manifest generated:
deployment/manifest.json

Contain of manifest.json:-

{
  "manifestSchemaVersion": "1.0.0",
  "artifacts": [
    {
      "artifactId": "commercial-domain-model",
      "version": "0.1.0",
      "file": "ontology/commercial-domain-model.ttl",
      "format": "turtle",
      "sha256": "abc123...",
      "approvalStatus": "approved",
      "approvedBy": "umesh.samal_ext@novartis.com",
      "sourceRef": "git:LOCAL-DEMO-001"
    }
  ]
}


 Simple explanation

Think of manifest.json as the deployment package's identity card.

It tells us:

What was deployed?
       ↓
commercial-domain-model

Which version?
       ↓
0.1.0

Which Git commit?
       ↓
LOCAL-DEMO-001

Who approved it?
       ↓
Reviewer

Is it approved?
       ↓
YES

What is the file checksum?
       ↓
SHA256

8. Step 6 — S3 Deployment

After approval and manifest generation, the final step is to upload:

commercial-domain-model.ttl
commercial-shapes.ttl
manifest.json

to the controlled S3 location.

Conceptually:

S3
└── ontology/
    └── commercial-domain-model/
        └── 0.1.0/
            ├── commercial-domain-model.ttl
            ├── commercial-shapes.ttl
            └── manifest.json


Simple explanation

"Only after validation and approval do we promote the ontology artifacts to the controlled S3 location consumed by downstream AWS components."

9. Complete POC flow

This is the most important diagram to show your manager:

                     ┌──────────────┐
                     │   Protégé    │
                     │ Ontology     │
                     │ Authoring     │
                     └──────┬───────┘
                            │
                            │ Git Push
                            ▼
                     ┌──────────────┐
                     │  Bitbucket   │
                     │ Version      │
                     │ Control      │
                     └──────┬───────┘
                            │
                            │ Pipeline Trigger
                            ▼
                     ┌──────────────┐
                     │   Jenkins    │
                     │              │
                     └──────┬───────┘
                            │
                            ▼
                  ┌────────────────────┐
                  │ SHACL Validation   │
                  └─────────┬──────────┘
                            │
                          PASS
                            │
                            ▼
                  ┌────────────────────┐
                  │ Identify Reviewer  │
                  └─────────┬──────────┘
                            │
                            ▼
                  ┌────────────────────┐
                  │ Send Email         │
                  │ Approval Request   │
                  └─────────┬──────────┘
                            │
                            ▼
                  ┌────────────────────┐
                  │ Reviewer Review    │
                  └─────────┬──────────┘
                            │
                         APPROVED
                            │
                            ▼
                  ┌────────────────────┐
                  │ Record Approval    │
                  │ + Commit SHA       │
                  └─────────┬──────────┘
                            │
                            ▼
                  ┌────────────────────┐
                  │ Generate Manifest  │
                  └─────────┬──────────┘
                            │
                            ▼
                  ┌────────────────────┐
                  │       S3           │
                  │ Approved Artifacts │
                  └────────────────────┘


"I created a POC for the proposed ontology approval workflow. The current implementation validates the ontology using SHACL, identifies the designated approver based on the ontology domain, and sends an automated email containing the ontology name, version, Git commit SHA, and review URL.

After approval, the POC records the approval information against the specific commit, including the approver and timestamp. It then generates a manifest containing the approved artifact details, version, Git reference, approval information, and checksum.

The next deployment step is to promote the approved ontology, SHACL file, and generated manifest to the controlled S3 location.

The intended end-to-end flow is Protégé → Bitbucket → Jenkins → SHACL validation → reviewer notification → approval → manifest generation → S3.

Currently, I have demonstrated the core workflow locally. The next step is to integrate the same scripts into Jenkins and connect the Bitbucket trigger and controlled S3 deployment."







