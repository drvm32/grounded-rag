# Baseline eval results

## [f1] (factual) What is the maximum item size allowed in a DynamoDB table?

**Expected:** 400 KB, including both attribute name and attribute value lengths.

**System answer:** The maximum item size in DynamoDB is 400 KB.

**Grade (fill in correct/incorrect):** 

---

## [f2] (factual) What is the minimum storage duration for the S3 Glacier Deep Archive storage class?

**Expected:** 180 days.

**System answer:** Based on the provided context, the minimum storage duration for the S3 Glacier Deep Archive storage class is 180 days.

**Grade (fill in correct/incorrect):** 

---

## [f3] (factual) How many local secondary indexes can a DynamoDB table have?

**Expected:** Up to 5 local secondary indexes per table.

**System answer:** Based on the context provided, you can define up to 5 local secondary indexes per table.

**Grade (fill in correct/incorrect):** 

---

## [f4] (factual) What is the default per-table read/write throughput quota for a DynamoDB on-demand table?

**Expected:** 40,000 read request units and 40,000 write request units.

**System answer:** Based on the provided context, the default per-table read/write throughput quota for a DynamoDB on-demand table is 40,000 read request units and 40,000 write request units.

**Grade (fill in correct/incorrect):** 

---

## [f5] (factual) What is the minimum billable object size for the S3 Standard-IA storage class?

**Expected:** 128 KB — smaller objects are still billed as if they were 128 KB.

**System answer:** Based on the provided context, the minimum billable object size for the S3 Standard-IA storage class is 128 KB (if an object is less than 128 KB, Amazon S3 charges you for 128 KB).

**Grade (fill in correct/incorrect):** 

---

## [f6] (factual) How many unique items can a single DynamoDB transaction contain?

**Expected:** No more than 100 unique items, and no more than 4 MB of data.

**System answer:** A transaction cannot contain more than 100 unique items.

**Grade (fill in correct/incorrect):** 

---

## [c1] (comparison) What's the practical difference between S3 Standard-IA and S3 One Zone-IA?

**Expected:** Standard-IA stores data redundantly across >= 3 Availability Zones and is resilient to the loss of an AZ; One Zone-IA stores data in only one AZ, is cheaper, but is not resilient to AZ loss.

**System answer:** Based on the provided context, the practical differences between S3 Standard-IA and S3 One Zone-IA include:

* **Data Storage and Resiliency:** S3 Standard-IA stores object data redundantly across multiple geographically separated Availability Zones and is resilient to the loss of an Availability Zone. In contrast, S3 One Zone-IA stores object data in only one Availability Zone, is not resilient to the physical loss of that Availability Zone resulting from disasters (such as earthquakes and floods), and is not resilient to the loss of the Availability Zone.
* **Availability and Cost:** S3 Standard-IA offers greater availability than S3 One Zone-IA (the context notes S3 One Zone-IA is "less available and less resilient"). Because S3 One Zone-IA stores data in only one Availability Zone, it is less expensive than S3 Standard-IA.
* **Recommended Use Cases:** 
  * S3 Standard-IA is recommended for your primary or only copy of data that cannot be re-created.
  * S3 One Zone-IA is recommended if you can re-create the data if the Availability Zone fails, for object replicas when configuring S3 Cross-Region Replication (CRR), and for data residency and isolation when creating directory buckets in AWS Local Zones.

**Grade (fill in correct/incorrect):** 

---

## [c2] (comparison) Should I use S3 Intelligent-Tiering or a manual lifecycle rule to S3 Standard-IA?

**Expected:** Use Intelligent-Tiering when access patterns are unknown or changing, since it auto-moves objects between tiers with no retrieval fees; use a manual lifecycle rule to Standard-IA when you already know the object will become infrequently accessed.

**System answer:** Based on the provided context, there is no information comparing whether you should use S3 Intelligent-Tiering or a manual lifecycle rule to S3 Standard-IA to answer this question.

**Grade (fill in correct/incorrect):** 

---

## [c3] (comparison) How do DynamoDB's account-level throughput quotas differ between on-demand and provisioned capacity mode?

**Expected:** Account-level read/write throughput quotas only apply to provisioned capacity mode tables; on-demand mode tables have no account-level throughput quota, only a table-level one.

**System answer:** Based on the provided context, account-level throughput quotas apply to the sum of the provisioned throughput capacity for all of an account's tables and global secondary indexes in a given Region, and they **only apply to tables using the provisioned capacity mode**. In contrast, **no account-level read and write throughput quotas are applied to tables in on-demand mode** (as indicated by "Not applicable" in the table and the statement that "No account-level read and write throughput quotas are applied to tables in on-demand mode").

**Grade (fill in correct/incorrect):** 

---

## [c4] (comparison) What's the difference between a local secondary index and a global secondary index in terms of item collection size limits?

**Expected:** A table with one or more local secondary indexes has item collections capped at 10GB because the LSI is colocated in the same partition as the base table; global secondary indexes are independent of the base table and not subject to that same-partition constraint.

**System answer:** Based on the provided context, for a table with one or more local secondary indexes (LSIs), item collections cannot exceed 10GB in size (which includes all base table items and all projected LSI views that share the same partition key attribute, as the item collection cannot be distributed to multiple partitions). 

However, regarding global secondary indexes (GSIs), the context only states that "in a global secondary index the item collection is independent of the base table (and can have a different partition key attribute)." The context does not provide a specific item collection size limit for global secondary indexes.

**Grade (fill in correct/incorrect):** 

---

## [c5] (comparison) What's the tradeoff between S3 Glacier Instant Retrieval and S3 Glacier Flexible Retrieval?

**Expected:** Glacier Instant Retrieval gives millisecond, real-time access for rarely-accessed data; Glacier Flexible Retrieval is cheaper but data is archived and requires a restore taking minutes to hours before it's accessible.

**System answer:** Based on the provided context, the differences and characteristics (tradeoffs) between the two are:

* **S3 Glacier Instant Retrieval (GLACIER_IR):** 
  * Used for long-lived, archive data accessed once a quarter.
  * Provides millisecond access / real-time access.
  * Per-GB retrieval fees apply.
* **S3 Glacier Flexible Retrieval (GLACIER):** 
  * Used for long-lived archive data accessed once a year.
  * Retrieval times take from minutes to hours.
  * Data is archived and *not* available for real-time access.

**Grade (fill in correct/incorrect):** 

---

## [c6] (comparison) What's the practical difference between EC2's Nitro and Xen hypervisors when choosing an instance type?

**Expected:** Nitro is used by current-generation instance types (e.g. M5, C6i, R7g); Xen is used only by previous-generation instance types (e.g. M1-M4, C1-C4, R3-R4), so Nitro is what you'd pick for anything modern.

**System answer:** The provided context does not contain information about the practical difference between EC2's Nitro and Xen hypervisors when choosing an instance type.

**Grade (fill in correct/incorrect):** 

---

## [o1] (operational) I tagged an S3 object to trigger a lifecycle transition, but now I want to cancel it before it runs. What should I do?

**Expected:** Remove the tag rather than disabling the rule, since rule policy updates can take up to 15 minutes to propagate; even then, cancellation isn't guaranteed because evaluation and execution timing aren't deterministic.

**System answer:** Based on the provided context, to prevent a transition before it executes, you should remove the tag rather than disabling the rule.

**Grade (fill in correct/incorrect):** 

---

## [o2] (operational) How should I restrict SSH access to my EC2 instance using security groups?

**Expected:** Add an inbound rule for port 22 that authorizes only specific IP address ranges — do not use 0.0.0.0/0 (or ::/0 for IPv6), which would allow access from any IP address.

**System answer:** Based on the provided context, you should authorize only specific IP address ranges rather than specifying 0.0.0.0/0 (IPv4) and ::/ (IPv6), which would enable anyone to access your instances. Additionally, you must ensure that access through each port is restricted to the sources or destinations that require it.

**Grade (fill in correct/incorrect):** 

---

## [o3] (operational) How do I move an object out of S3 Glacier Deep Archive back to S3 Standard?

**Expected:** You can't do it with a Lifecycle rule directly — Glacier Deep Archive transitions only go one way. You must first restore a temporary copy of the object, then use a copy operation to overwrite it specifying S3 Standard as the destination storage class.

**System answer:** Based on the provided context, if you want to change the storage class of an archived object from S3 Glacier Deep Archive to another storage class (such as S3 Standard), you must use the restore operation to make a temporary copy of the object first. Then, use the copy operation to overwrite the object specifying S3 Standard.

**Grade (fill in correct/incorrect):** 

---

## [o4] (operational) My DynamoDB BatchWriteItem call includes 30 PutItem requests. Will it succeed?

**Expected:** No — a single BatchWriteItem operation can contain at most 25 PutItem or DeleteItem requests, so 30 requests exceeds the limit.

**System answer:** No, it will not succeed. A single BatchWriteItem operation can contain up to 25 PutItem or DeleteItem requests, and your call includes 30.

**Grade (fill in correct/incorrect):** 

---

## [o5] (operational) How many times per day can I decrease provisioned throughput on a DynamoDB table?

**Expected:** You start each day (UTC) with 4 available decreases, plus 1 more becomes available each hour up to a max of 4 available at any time — allowing up to 27 decreases over a full 24-hour day.

**System answer:** Based on the provided context, over a full 24-hour day, you are allowed to decrease up to 27 times (4 in the first hour, plus 1 for each of the remaining 23 hours).

**Grade (fill in correct/incorrect):** 

---

## [o6] (operational) I need more than 2,500 DynamoDB tables in one AWS account/region. What are my options?

**Expected:** You can contact your AWS account team to request an increase up to a maximum of 10,000 tables per account/region; beyond 10,000, the recommended practice is to use multiple accounts.

**System answer:** Based on the provided context, your options are:

* Reach out to your AWS account team to explore an increase up to a maximum of 10,000 tables.
* If you need more than 10,000 tables, the recommended best practice is to set up multiple accounts, each of which can serve up to 10,000 tables.

**Grade (fill in correct/incorrect):** 

---
