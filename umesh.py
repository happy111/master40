

 Validate ontology

1. python scripts/validate_antology.py

   Find reviewer

2. python scripts/identify_approver.py
  
    send email
3.  python scripts/send_approval_email.py --approver "umesh.samal_ext@novartis.com" --ontology "commercial-domain-model" --version "0.1.0" --commit "LOCAL-DEMO-001" --url "https://your-git-server/your-repository/commit/LOCAL-DEMO-001"

4. Approval

   python scripts/approval.py --approve --approver "reviewer@example.com" --commit "ASS"

5 . Generate manifest file

    python scripts/generate_manifest.py

6. 
