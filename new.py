https://chatgpt.com/c/6a8557eb-760c-83e9-a3b9-03b7ba220d04




default_reviewers:
  - name: Commercial Reviewer
    email: reviewer@example.com
    bitbucket_uuid: "{00000000-0000-0000-0000-000000000001}"

# If any changed TTL file path contains a pattern, these reviewers are added.
domain_reviewers:
  commercial:
    patterns:
      - "commercial"
      - "ontology/commercial"
    reviewers:
      - name: Commercial SME
        email: commercial-reviewer@example.com
        bitbucket_uuid: "{00000000-0000-0000-0000-000000000002}"

custom_notification_emails:
  - architecture-team@example.com












Developer pushes TTL changes to feature branch
        ↓
Jenkins detects change (webhook)
        ↓
 Generates manifest.json
        ↓
2. Commits manifest
        ↓
3. Pushes to Bitbucket (same feature branch)
        ↓
4. Creates PR automatically (develop ← feature branch)
        ↓
5. Assigns reviewers
        ↓
6. Sends email to reviewers(default email + custom email)
        ↓
Reviewers review in PR + approve
        ↓
Merge to develop 
        ↓
Trigger the second Jenkins pipeline using webhook to copy the added/updated ttl files(incremental changes) and manifest file(s) from the develop branch to the s3 bucket in the required folder structure
