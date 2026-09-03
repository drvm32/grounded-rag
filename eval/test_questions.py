"""
Test question bank for grounded-rag evaluation (steps 6, 7, 9).

Each question has:
  id             - short stable identifier
  group          - one of: factual, comparison, operational, unanswerable
  question       - the question text to send to the workflow
  expected_answer- the answer you've manually verified from the corpus,
                    used for your own side-by-side grading (not automated matching)
  source         - which file(s) the answer should be grounded in (None for unanswerable)
"""

QUESTIONS = [
    # ---- Group 1: precise factual limits ----
    {
        "id": "f1",
        "group": "factual",
        "question": "What is the maximum item size allowed in a DynamoDB table?",
        "expected_answer": "400 KB, including both attribute name and attribute value lengths.",
        "source": "dynamodb_constraints.txt",
    },
    {
        "id": "f2",
        "group": "factual",
        "question": "What is the minimum storage duration for the S3 Glacier Deep Archive storage class?",
        "expected_answer": "180 days.",
        "source": "s3_storage_classes.txt",
    },
    {
        "id": "f3",
        "group": "factual",
        "question": "How many local secondary indexes can a DynamoDB table have?",
        "expected_answer": "Up to 5 local secondary indexes per table.",
        "source": "dynamodb_quotas.txt",
    },
    {
        "id": "f4",
        "group": "factual",
        "question": "What is the default per-table read/write throughput quota for a DynamoDB on-demand table?",
        "expected_answer": "40,000 read request units and 40,000 write request units.",
        "source": "dynamodb_quotas.txt",
    },
    {
        "id": "f5",
        "group": "factual",
        "question": "What is the minimum billable object size for the S3 Standard-IA storage class?",
        "expected_answer": "128 KB. Smaller objects are still billed as if they were 128 KB.",
        "source": "s3_storage_classes.txt",
    },
    {
        "id": "f6",
        "group": "factual",
        "question": "How many unique items can a single DynamoDB transaction contain?",
        "expected_answer": "No more than 100 unique items, and no more than 4 MB of data.",
        "source": "dynamodb_constraints.txt",
    },

    # ---- Group 2: comparison / tradeoff ----
    {
        "id": "c1",
        "group": "comparison",
        "question": "What's the practical difference between S3 Standard-IA and S3 One Zone-IA?",
        "expected_answer": "Standard-IA stores data redundantly across >= 3 Availability Zones and is resilient to the loss of an AZ; One Zone-IA stores data in only one AZ, is cheaper, but is not resilient to AZ loss.",
        "source": "s3_storage_classes.txt",
    },
    {
        "id": "c2",
        "group": "comparison",
        "question": "Should I use S3 Intelligent-Tiering or a manual lifecycle rule to S3 Standard-IA?",
        "expected_answer": "Use Intelligent-Tiering when access patterns are unknown or changing, since it auto-moves objects between tiers with no retrieval fees; use a manual lifecycle rule to Standard-IA when you already know the object will become infrequently accessed.",
        "source": "s3_storage_classes.txt",
    },
    {
        "id": "c3",
        "group": "comparison",
        "question": "How do DynamoDB's account-level throughput quotas differ between on-demand and provisioned capacity mode?",
        "expected_answer": "Account-level read/write throughput quotas only apply to provisioned capacity mode tables; on-demand mode tables have no account-level throughput quota, only a table-level one.",
        "source": "dynamodb_quotas.txt",
    },
    {
        "id": "c4",
        "group": "comparison",
        "question": "What's the difference between a local secondary index and a global secondary index in terms of item collection size limits?",
        "expected_answer": "A table with one or more local secondary indexes has item collections capped at 10GB because the LSI is colocated in the same partition as the base table; global secondary indexes are independent of the base table and not subject to that same-partition constraint.",
        "source": "dynamodb_constraints.txt",
    },
    {
        "id": "c5",
        "group": "comparison",
        "question": "What's the tradeoff between S3 Glacier Instant Retrieval and S3 Glacier Flexible Retrieval?",
        "expected_answer": "Glacier Instant Retrieval gives millisecond, real-time access for rarely-accessed data; Glacier Flexible Retrieval is cheaper but data is archived and requires a restore taking minutes to hours before it's accessible.",
        "source": "s3_storage_classes.txt",
    },
    {
        "id": "c6",
        "group": "comparison",
        "question": "What's the practical difference between EC2's Nitro and Xen hypervisors when choosing an instance type?",
        "expected_answer": "Nitro is used by current-generation instance types (e.g. M5, C6i, R7g); Xen is used only by previous-generation instance types (e.g. M1-M4, C1-C4, R3-R4), so Nitro is what you'd pick for anything modern.",
        "source": "ec2_instance_types.txt",
    },

    # ---- Group 3: operational / practical ----
    {
        "id": "o1",
        "group": "operational",
        "question": "I tagged an S3 object to trigger a lifecycle transition, but now I want to cancel it before it runs. What should I do?",
        "expected_answer": "Remove the tag rather than disabling the rule, since rule policy updates can take up to 15 minutes to propagate; even then, cancellation isn't guaranteed because evaluation and execution timing aren't deterministic.",
        "source": "s3_transitions.txt",
    },
    {
        "id": "o2",
        "group": "operational",
        "question": "How should I restrict SSH access to my EC2 instance using security groups?",
        "expected_answer": "Add an inbound rule for port 22 that authorizes only specific IP address ranges. Do not use 0.0.0.0/0 (or ::/0 for IPv6), which would allow access from any IP address.",
        "source": "ec2_security_groups.txt",
    },
    {
        "id": "o3",
        "group": "operational",
        "question": "How do I move an object out of S3 Glacier Deep Archive back to S3 Standard?",
        "expected_answer": "You can't do it with a Lifecycle rule directly, since Glacier Deep Archive transitions only go one way. You must first restore a temporary copy of the object, then use a copy operation to overwrite it specifying S3 Standard as the destination storage class.",
        "source": "s3_transitions.txt",
    },
    {
        "id": "o4",
        "group": "operational",
        "question": "My DynamoDB BatchWriteItem call includes 30 PutItem requests. Will it succeed?",
        "expected_answer": "No. A single BatchWriteItem operation can contain at most 25 PutItem or DeleteItem requests, so 30 requests exceeds the limit.",
        "source": "dynamodb_constraints.txt",
    },
    {
        "id": "o5",
        "group": "operational",
        "question": "How many times per day can I decrease provisioned throughput on a DynamoDB table?",
        "expected_answer": "You start each day (UTC) with 4 available decreases, plus 1 more becomes available each hour up to a max of 4 available at any time. That allows up to 27 decreases over a full 24-hour day.",
        "source": "dynamodb_quotas.txt",
    },
    {
        "id": "o6",
        "group": "operational",
        "question": "I need more than 2,500 DynamoDB tables in one AWS account/region. What are my options?",
        "expected_answer": "You can contact your AWS account team to request an increase up to a maximum of 10,000 tables per account/region; beyond 10,000, the recommended practice is to use multiple accounts.",
        "source": "dynamodb_quotas.txt",
    },

    # ---- Group 4: not in local corpus, but answerable via live web search fallback ----
    # (not counted in early hit-rate; these exercise the web_search() correction path,
    #  not the refusal path, see the "refusal" group below for that)
    {
        "id": "u1",
        "group": "web_fallback",
        "question": "What is the price per GB-month for S3 Standard storage in the us-east-1 region?",
        "expected_answer": "Not in the local corpus, but a real, publicly documented figure. Should be answered via web search fallback with a cited source.",
        "source": None,
    },
    {
        "id": "u2",
        "group": "web_fallback",
        "question": "How do I configure an EC2 Auto Scaling Group to scale based on CPU utilization?",
        "expected_answer": "Not in the local corpus, but a real, publicly documented AWS feature. Should be answered via web search fallback with a cited source.",
        "source": None,
    },
    {
        "id": "u3",
        "group": "web_fallback",
        "question": "Can a DynamoDB Stream trigger an AWS Lambda function, and if so, how many concurrent executions are allowed?",
        "expected_answer": "Not in the local corpus, but a real, publicly documented integration. Should be answered via web search fallback with a cited source.",
        "source": None,
    },
    {
        "id": "u4",
        "group": "web_fallback",
        "question": "How does Multi-AZ failover work for an Amazon RDS database instance?",
        "expected_answer": "Not in the local corpus (RDS is a different service), but a real, publicly documented mechanism. Should be answered via web search fallback with a cited source.",
        "source": None,
    },
    {
        "id": "u5",
        "group": "web_fallback",
        "question": "What SLA uptime percentage does AWS guarantee for EC2 instances?",
        "expected_answer": "Not in the local corpus, but a real, publicly documented SLA figure. Should be answered via web search fallback with a cited source.",
        "source": None,
    },
    {
        "id": "u6",
        "group": "web_fallback",
        "question": "How do I set up a cross-account IAM role to let another AWS account access my S3 bucket?",
        "expected_answer": "Not in the local corpus, but a real, publicly documented procedure. Should be answered via web search fallback with a cited source.",
        "source": None,
    },

    # ---- Group 5: genuinely unanswerable (neither local corpus nor web search can answer) ----
    # these test the actual "I don't know" refusal path
    {
        "id": "r1",
        "group": "refusal",
        "question": "What is the maximum throughput of AWS's 'S3 Quantum Storage' tier?",
        "expected_answer": "I don't know / refusal. 'S3 Quantum Storage' is not a real AWS storage class, so no source (local or web) should have an answer.",
        "source": None,
    },
    {
        "id": "r2",
        "group": "refusal",
        "question": "How much free storage capacity is currently remaining in my personal S3 bucket named 'my-prod-backups-2026'?",
        "expected_answer": "I don't know / refusal. This is private, account-specific data that no public document or web search could know.",
        "source": None,
    },
    {
        "id": "r3",
        "group": "refusal",
        "question": "What was the exact CPU utilization, minute-by-minute, of EC2 instance i-0123456789abcdef0 last Tuesday?",
        "expected_answer": "I don't know / refusal. This is private CloudWatch metric data specific to one AWS account, not publicly available anywhere.",
        "source": None,
    },
]
