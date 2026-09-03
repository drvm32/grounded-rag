# Baseline eval results

## [f1] (factual) What is the maximum item size allowed in a DynamoDB table?

**Expected:** 400 KB, including both attribute name and attribute value lengths.

**System answer:** The maximum item size allowed in a DynamoDB table is 400 KB [Source: data\DynamoDB\dynamodb_constraints.txt, Source: https://repost.aws/questions/QULMEWExVGSLaax5GwNYbpvQ/maximum-item-size-in-dynamodb-for-storing-base64-images, Source: https://dynobase.dev/dynamodb-limits].

**Grade (fill in correct/incorrect):** correct

---

## [f2] (factual) What is the minimum storage duration for the S3 Glacier Deep Archive storage class?

**Expected:** 180 days.

**System answer:** The minimum storage duration for the S3 Glacier Deep Archive storage class is 180 days [Source: data\S3\s3_storage_classes.txt; data\S3\s3_transitions.txt; https://docs.aws.amazon.com/AmazonS3/latest/userguide/glacier-storage-classes.html; https://docs.aws.amazon.com/AmazonS3/latest/userguide/archival-storage.html; https://repost.aws/questions/QUtbRe7EVOR1G9P30SFPn6CQ/understanding-s3-glacier-deep-and-is-it-safe-to-delete].

**Grade (fill in correct/incorrect):** correct

---

## [f3] (factual) How many local secondary indexes can a DynamoDB table have?

**Expected:** Up to 5 local secondary indexes per table.

**System answer:** Based on the provided context, a DynamoDB table can have up to 5 local secondary indexes [Source: data\DynamoDB\dynamodb_quotas.txt, Source: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-indexes-general.html, Source: https://www.youtube.com/watch?v=ki5Z1ZfYLFk].

**Grade (fill in correct/incorrect):** correct

---

## [f4] (factual) What is the default per-table read/write throughput quota for a DynamoDB on-demand table?

**Expected:** 40,000 read request units and 40,000 write request units.

**System answer:** Based on the provided context, the default per-table throughput quota for an on-demand DynamoDB table is 40,000 read request units and 40,000 write request units [data\DynamoDB\dynamodb_quotas.txt, https://www.amazonaws.cn/en/new/2024/amazon-dynamodb-introduces-configurable-maximum-throughput-for-on-demand-tables, https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ServiceQuotas.html].

**Grade (fill in correct/incorrect):** correct

---

## [f5] (factual) What is the minimum billable object size for the S3 Standard-IA storage class?

**Expected:** 128 KB — smaller objects are still billed as if they were 128 KB.

**System answer:** Based on the provided context, the minimum billable object size for the S3 Standard-IA storage class is 128 KB [data\S3\s3_storage_classes.txt, https://aws.amazon.com/s3/pricing, https://repost.aws/questions/QUiT9aLCJZQzygJ2z80UChNw/minimum-object-size-of-128kb-at-one-zone-infrequent-access-storage-class, https://cloudian.com/blog/5-components-of-aws-s3-storage-pricing].

**Grade (fill in correct/incorrect):** correct

---

## [f6] (factual) How many unique items can a single DynamoDB transaction contain?

**Expected:** No more than 100 unique items, and no more than 4 MB of data.

**System answer:** Based on the provided context, a DynamoDB transaction cannot contain more than 100 unique items [Source: data\DynamoDB\dynamodb_constraints.txt]. However, another source notes that a transaction supports a maximum of 25 items [Source: https://urielbitton.substack.com/p/5-common-mistakes-when-using-dynamodb], while a StackOverflow discussion mentions a limit of 25 items [Source: https://stackoverflow.com/questions/61160447/is-there-a-way-to-work-around-the-transaction-item-limit-in-dynamodb] as well as 100 items per request/transaction [Source: https://stackoverflow.com/questions/61160447/is-there-a-way-to-work-around-the-transaction-item-limit-in-dynamodb, Source: https://github.com/awslabs/dynamodb-transactions/issues/53].

**Grade (fill in correct/incorrect):** incorrect - web search added contradictory noise (25-item BatchWriteItem limit mixed into the 100-item transaction answer)

---

## [c1] (comparison) What's the practical difference between S3 Standard-IA and S3 One Zone-IA?

**Expected:** Standard-IA stores data redundantly across >= 3 Availability Zones and is resilient to the loss of an AZ; One Zone-IA stores data in only one AZ, is cheaper, but is not resilient to AZ loss.

**System answer:** Based on the provided context, the practical differences between S3 Standard-IA and S3 One Zone-IA include:

* **Data Storage and Redundancy:** S3 Standard-IA stores object data redundantly across multiple geographically separated Availability Zones (at least 3 AZs) [data\S3\s3_storage_classes.txt, https://www.reddit.com/r/AWSCertifications/comments/yykzlq/aws_ia_vs_one_zone_ia]. In contrast, S3 One Zone-IA stores object data in only one Availability Zone [data\S3\s3_storage_classes.txt, https://www.whizlabs.com/blog/s3-one-zone-ia-vs-s3-standard-ia].
* **Resiliency and Availability:** S3 Standard-IA objects are resilient to the loss of an Availability Zone and offer greater availability and resiliency [data\S3\s3_storage_classes.txt]. S3 One Zone-IA is less available, less resilient, and not resilient to the physical loss of its Availability Zone from disasters like earthquakes and floods (though it matches S3 Standard-IA in durability) [data\S3\s3_storage_classes.txt].
* **Cost:** S3 One Zone-IA is less expensive than S3 Standard-IA [data\S3\s3_storage_classes.txt, https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage-class-intro.html].
* **Recommended Use Cases:** 
  * **S3 Standard-IA** is recommended for a primary or only copy of data that cannot be re-created [data\S3\s3_storage_classes.txt, https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage-class-intro.html].
  * **S3 One Zone-IA** is recommended if the data can be re-created if the Availability Zone fails, for object replicas when configuring S3 Cross-Region Replication (CRR), and for data residency and isolation when creating directory buckets in AWS Local Zones [data\S3\s3_storage_classes.txt, https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage-class-intro.html].

**Grade (fill in correct/incorrect):** correct

---

## [c2] (comparison) Should I use S3 Intelligent-Tiering or a manual lifecycle rule to S3 Standard-IA?

**Expected:** Use Intelligent-Tiering when access patterns are unknown or changing, since it auto-moves objects between tiers with no retrieval fees; use a manual lifecycle rule to Standard-IA when you already know the object will become infrequently accessed.

**System answer:** Based on the provided context, you should choose based on your access patterns and management preferences:

* **Use S3 Intelligent-Tiering** when your data access patterns are unpredictable or mixed, and you want automatic tier management that requires no manual lifecycle rules and charges no retrieval fees [Source: https://sedai.io/blog/amazon-s3-intelligent-tiering-storage-optimization].
* **Use S3 Standard-IA** when your data access is consistently infrequent and predictable. S3 Standard-IA has lower per-object overhead, but it requires manual lifecycle rules to transition data and charges retrieval fees [Source: https://sedai.io/blog/amazon-s3-intelligent-tiering-storage-optimization].

**Grade (fill in correct/incorrect):** correct

---

## [c3] (comparison) How do DynamoDB's account-level throughput quotas differ between on-demand and provisioned capacity mode?

**Expected:** Account-level read/write throughput quotas only apply to provisioned capacity mode tables; on-demand mode tables have no account-level throughput quota, only a table-level one.

**System answer:** Based on the provided context, the account-level throughput quotas differ between the two capacity modes as follows:

* **Provisioned Capacity Mode:** Account-level read and write throughput quotas apply to the sum of the provisioned throughput capacity for all of an account's tables and global secondary indexes in a given Region (these account-level quotas are initially set at 80,000 read capacity units and 80,000 write capacity units by default, and are adjustable) [data\DynamoDB\dynamodb_quotas.txt, https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ServiceQuotas.html].
* **On-Demand Capacity Mode:** No account-level read and write throughput quotas are applied to tables in on-demand mode (listed as "Not applicable" for the per-account quota) [data\DynamoDB\dynamodb_quotas.txt, https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ServiceQuotas.html].

**Grade (fill in correct/incorrect):** correct

---

## [c4] (comparison) What's the difference between a local secondary index and a global secondary index in terms of item collection size limits?

**Expected:** A table with one or more local secondary indexes has item collections capped at 10GB because the LSI is colocated in the same partition as the base table; global secondary indexes are independent of the base table and not subject to that same-partition constraint.

**System answer:** Based on the provided context, the differences in item collection size limits between a local secondary index (LSI) and a global secondary index (GSI) are:

* **Local Secondary Indexes (LSIs):** Tables with one or more LSIs are subject to an item collection size limit. No single item collection (consisting of all items in the base table and its LSIs that share the same partition key) can exceed 10 GB in size, as each item collection is stored in a single partition whose maximum size is 10 GB [data\DynamoDB\dynamodb_constraints.txt, https://www.dynamodbguide.com/local-or-global-choosing-a-secondary-index-type-in-dynamo-db, https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/LSI.html]. 
* **Global Secondary Indexes (GSIs):** GSIs do not have item collection size limits [https://www.dynamodbguide.com/local-or-global-choosing-a-secondary-index-type-in-dynamo-db, https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/LSI.html].

**Grade (fill in correct/incorrect):** correct

---

## [c5] (comparison) What's the tradeoff between S3 Glacier Instant Retrieval and S3 Glacier Flexible Retrieval?

**Expected:** Glacier Instant Retrieval gives millisecond, real-time access for rarely-accessed data; Glacier Flexible Retrieval is cheaper but data is archived and requires a restore taking minutes to hours before it's accessible.

**System answer:** Based on the provided context, the tradeoffs between S3 Glacier Instant Retrieval and S3 Glacier Flexible Retrieval involve access speed, retrieval methods, costs, and availability for real-time access:

* **Retrieval Speed and Access:** 
  * **S3 Glacier Instant Retrieval** provides millisecond access and is available for real-time access [data\S3\s3_storage_classes.txt, https://www.rabinarayanpatra.com/blogs/s3-glacier-instant-vs-flexible-vs-deep-archive]. 
  * **S3 Glacier Flexible Retrieval** is archived and not available for real-time access; it requires asynchronous retrieval times ranging from minutes to hours (offering expedited retrievals in 1–5 minutes, standard retrievals in 3–5 hours, and free bulk retrievals in 5–12 hours) [data\S3\s3_storage_classes.txt, https://aws.amazon.com/s3/storage-classes/glacier].
* **Storage and Retrieval Costs:** 
  * **S3 Glacier Instant Retrieval** has a higher storage cost (e.g., $0.004 per GB compared to Flexible Retrieval's $0.0036 per GB) and applies per-GB retrieval fees, but allows for immediate, direct GET requests [data\S3\s3_storage_classes.txt, https://amazonwebshark.com/s3-glacier-instant-retrieval-first-impressions, https://www.rabinarayanpatra.com/blogs/s3-glacier-instant-vs-flexible-vs-deep-archive].
  * **S3 Glacier Flexible Retrieval** delivers storage up to 10% lower in cost than Instant Retrieval and provides the flexibility to retrieve large sets of data with free bulk retrievals, though its PUT/COPY/POST/LIST request costs can be significantly higher [https://aws.amazon.com/s3/storage-classes/glacier, https://amazonwebshark.com/s3-glacier-instant-retrieval-first-impressions]. 
* **Use Cases:** 
  * **Instant Retrieval** is best for long-lived data accessed about once a quarter that requires immediate, instant loading (such as medical images or news media archives) [data\S3\s3_storage_classes.txt, https://www.rabinarayanpatra.com/blogs/s3-glacier-instant-vs-flexible-vs-deep-archive].
  * **Flexible Retrieval** is best for backups, disaster recovery, or large datasets read once or twice a year where you can afford to wait minutes to hours for data to be restored [https://www.rabinarayanpatra.com/blogs/s3-glacier-instant-vs-flexible-vs-deep-archive, https://aws.amazon.com/s3/storage-classes/glacier].

**Grade (fill in correct/incorrect):** correct

---

## [c6] (comparison) What's the practical difference between EC2's Nitro and Xen hypervisors when choosing an instance type?

**Expected:** Nitro is used by current-generation instance types (e.g. M5, C6i, R7g); Xen is used only by previous-generation instance types (e.g. M1-M4, C1-C4, R3-R4), so Nitro is what you'd pick for anything modern.

**System answer:** Based on the provided context, the practical considerations and differences regarding hypervisors when choosing an instance type include:

* **AMI and Driver Compatibility:** Older AMIs do not provide NVMe drivers and rely on Xen-specific device naming, which is incompatible with newer Nitro-based instance types [Source: https://perspectives.mvdirona.com/2021/11/xen-on-nitro-aws-nitro-for-legacy-instances]. 
* **Virtualization and Generation Support:** Current generation instance types support hardware virtual machine (HVM) only, while some previous generation instance types support paravirtual (PV) [Source: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-types.html].
* **Legacy vs. Newer Workloads:** Customers using older, legacy instance types often rely on Xen-based instances because they prefer not to invest in upgrading their operating systems, whereas newer instances leverage the AWS Nitro System (a combination of dedicated hardware and a lightweight hypervisor) [Source: https://perspectives.mvdirona.com/2021/11/xen-on-nitro-aws-nitro-for-legacy-instances, Source: https://www.amazonaws.cn/en/ec2/instance-types].
* **Testing:** Because you pay by the second, you can easily test multiple instance types before deciding, and you can change your instance type later if your needs change [Source: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-types.html].

**Grade (fill in correct/incorrect):** correct

---

## [o1] (operational) I tagged an S3 object to trigger a lifecycle transition, but now I want to cancel it before it runs. What should I do?

**Expected:** Remove the tag rather than disabling the rule, since rule policy updates can take up to 15 minutes to propagate; even then, cancellation isn't guaranteed because evaluation and execution timing aren't deterministic.

**System answer:** To prevent a lifecycle transition before it executes, you should remove the tag rather than disabling the rule (since rule policy updates can take up to 15 minutes to propagate) [Source: data\S3\s3_transitions.txt, Source: https://docs.aws.amazon.com/AmazonS3/latest/userguide/lifecycle-transition-general-considerations.html]. However, because the time between evaluation and execution is not deterministic, removing the tag does not guarantee an immediate cancellation; the action may still execute before the tag removal is observed, or the tag removal may take effect before the next evaluation cycle. To reliably prevent a transition after tagging an object, you should wait for a Lifecycle Event Notification confirming that the action has completed before removing the tag.

**Grade (fill in correct/incorrect):** correct (re-run after network failure on first attempt)

---

## [o2] (operational) How should I restrict SSH access to my EC2 instance using security groups?

**Expected:** Add an inbound rule for port 22 that authorizes only specific IP address ranges — do not use 0.0.0.0/0 (or ::/0 for IPv6), which would allow access from any IP address.

**System answer:** To restrict SSH access to your EC2 instance using security groups, you should follow these guidelines:

* Authorize only specific IP address ranges or trusted entities rather than using unrestricted access like `0.0.0.0/0` (IPv4) or `::/0` (IPv6), which allows anyone to access your instances from any IP address [data\EC2\ec2_security_groups.txt, https://trendmicro.com/trendaivisiononecloudriskmanagement/knowledge-base/aws/EC2/unrestricted-ssh-access.html]. 
* Limit access to a specific IP address, or at the very least, to an IP address range associated with your corporate VPN so that instances can only be remotely managed from specific locations [https://awsinsider.net/articles/2026/02/03/best-practices-for-ec2-security-groups.aspx].

**Grade (fill in correct/incorrect):** correct

---

## [o3] (operational) How do I move an object out of S3 Glacier Deep Archive back to S3 Standard?

**Expected:** You can't do it with a Lifecycle rule directly — Glacier Deep Archive transitions only go one way. You must first restore a temporary copy of the object, then use a copy operation to overwrite it specifying S3 Standard as the destination storage class.

**System answer:** To move an object out of S3 Glacier Deep Archive to another storage class like S3 Standard, you cannot use an S3 Lifecycle configuration rule [data\S3\s3_transitions.txt, https://docs.aws.amazon.com/AmazonS3/latest/userguide/lifecycle-transition-general-considerations.html]. Instead, you must follow these steps:

1. **Use the restore operation** (or submit a restore request) to make a temporary copy of the object [data\S3\s3_transitions.txt, https://rcdsdocs.it.northwestern.edu/tutorials/cloud/aws/archiving-data-amazon-S3.html, https://docs.aws.amazon.com/AmazonS3/latest/userguide/lifecycle-transition-general-considerations.html]. 
2. **Use the copy operation** to overwrite the object while specifying S3 Standard as the desired storage class [data\S3\s3_transitions.txt, https://docs.aws.amazon.com/AmazonS3/latest/userguide/lifecycle-transition-general-considerations.html].

Sources:
- `data\S3\s3_transitions.txt`
- `https://rcdsdocs.it.northwestern.edu/tutorials/cloud/aws/archiving-data-amazon-S3.html`
- `https://docs.aws.amazon.com/AmazonS3/latest/userguide/lifecycle-transition-general-considerations.html`

**Grade (fill in correct/incorrect):** correct

---

## [o4] (operational) My DynamoDB BatchWriteItem call includes 30 PutItem requests. Will it succeed?

**Expected:** No — a single BatchWriteItem operation can contain at most 25 PutItem or DeleteItem requests, so 30 requests exceeds the limit.

**System answer:** No, your `BatchWriteItem` call will not succeed. A single `BatchWriteItem` operation can only process or contain up to 25 items (or PutItem/DeleteItem requests) per request, and exceeding this limit will cause the operation to fail [Source: data\DynamoDB\dynamodb_constraints.txt, Source: https://dynobase.dev/dynamodb-errors/dynamodb-batchwriteitem-error, Source: https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_BatchWriteItem.html].

**Grade (fill in correct/incorrect):** correct

---

## [o5] (operational) How many times per day can I decrease provisioned throughput on a DynamoDB table?

**Expected:** You start each day (UTC) with 4 available decreases, plus 1 more becomes available each hour up to a max of 4 available at any time — allowing up to 27 decreases over a full 24-hour day.

**System answer:** You can decrease provisioned throughput on a DynamoDB table up to 27 times per UTC day [data\DynamoDB\dynamodb_quotas.txt, https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ServiceQuotas.html]. You start each day with 4 available decreases, and 1 additional decrease becomes available each hour (up to a maximum of 4 available at any time), allowing for a total of up to 27 decreases over a full 24-hour day [data\DynamoDB\dynamodb_quotas.txt, https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ServiceQuotas.html, https://urielbitton.substack.com/p/understanding-dynamodb-throughput, https://repost.aws/knowledge-center/dynamodb-auto-scaling].

**Grade (fill in correct/incorrect):** correct

---

## [o6] (operational) I need more than 2,500 DynamoDB tables in one AWS account/region. What are my options?

**Expected:** You can contact your AWS account team to request an increase up to a maximum of 10,000 tables per account/region; beyond 10,000, the recommended practice is to use multiple accounts.

**System answer:** Based on the provided context, if you need more than 2,500 DynamoDB tables in one AWS account/region, your options are:

* You can reach out to your AWS account team to explore an increase up to a maximum of 10,000 tables [data\DynamoDB\dynamodb_quotas.txt].
* For more than 10,000 tables, the recommended best practice is to set up multiple accounts, with each account serving up to 10,000 tables [data\DynamoDB\dynamodb_quotas.txt].

**Grade (fill in correct/incorrect):** correct

---
