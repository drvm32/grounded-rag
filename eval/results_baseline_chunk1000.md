# Baseline eval results

## [f1] (factual) What is the maximum item size allowed in a DynamoDB table?

**Expected:** 400 KB, including both attribute name and attribute value lengths.

**System answer:** The maximum item size in a DynamoDB table is 400 KB.

**Grade (fill in correct/incorrect):** 

---

## [f2] (factual) What is the minimum storage duration for the S3 Glacier Deep Archive storage class?

**Expected:** 180 days.

**System answer:** Based on the context provided, the minimum storage duration for the S3 Glacier Deep Archive storage class is 180 days.

**Grade (fill in correct/incorrect):** 

---

## [f3] (factual) How many local secondary indexes can a DynamoDB table have?

**Expected:** Up to 5 local secondary indexes per table.

**System answer:** Based on the provided context, there is no mention of the maximum number of local secondary indexes a DynamoDB table can have.

**Grade (fill in correct/incorrect):** 

---

## [f4] (factual) What is the default per-table read/write throughput quota for a DynamoDB on-demand table?

**Expected:** 40,000 read request units and 40,000 write request units.

**System answer:** Based on the provided context, the default per-table throughput quota for an on-demand table is 40,000 read request units and 40,000 write request units.

**Grade (fill in correct/incorrect):** 

---

## [f5] (factual) What is the minimum billable object size for the S3 Standard-IA storage class?

**Expected:** 128 KB — smaller objects are still billed as if they were 128 KB.

**System answer:** 128 KB

**Grade (fill in correct/incorrect):** 

---

## [f6] (factual) How many unique items can a single DynamoDB transaction contain?

**Expected:** No more than 100 unique items, and no more than 4 MB of data.

**System answer:** A transaction cannot contain more than 100 unique items.

**Grade (fill in correct/incorrect):** 

---

## [c1] (comparison) What's the practical difference between S3 Standard-IA and S3 One Zone-IA?

**Expected:** Standard-IA stores data redundantly across >= 3 Availability Zones and is resilient to the loss of an AZ; One Zone-IA stores data in only one AZ, is cheaper, but is not resilient to AZ loss.

**System answer:** Based on the provided context, the practical differences between S3 Standard-IA and S3 One Zone-IA are:

* **Availability Zones & Cost:** S3 Standard-IA stores object data redundantly across multiple (>= 3) geographically separated Availability Zones, making it resilient to the loss of an Availability Zone. S3 One Zone-IA stores object data in only one Availability Zone, which makes it less expensive than S3 Standard-IA.
* **Resiliency and Availability:** S3 Standard-IA offers greater availability and resiliency. S3 One Zone-IA is less available, less resilient, and is *not* resilient to the physical loss of the Availability Zone resulting from disasters (such as earthquakes and floods). 
* **Data Residency:** For data residency and isolation use cases, S3 One Zone-IA (along with S3 Express One Zone) allows you to create directory buckets in AWS Local Zones, whereas S3 Standard-IA is not mentioned for this specific use. 
*(Note: Both storage classes share the same durability, millisecond access, and are designed for long-lived, infrequently accessed data, but the context does not provide a full comparison table for S3 One Zone-IA's specific metrics like min storage duration or min billable size).*

**Grade (fill in correct/incorrect):** 

---

## [c2] (comparison) Should I use S3 Intelligent-Tiering or a manual lifecycle rule to S3 Standard-IA?

**Expected:** Use Intelligent-Tiering when access patterns are unknown or changing, since it auto-moves objects between tiers with no retrieval fees; use a manual lifecycle rule to Standard-IA when you already know the object will become infrequently accessed.

**System answer:** The provided context does not contain the answer to this question.

**Grade (fill in correct/incorrect):** 

---

## [c3] (comparison) How do DynamoDB's account-level throughput quotas differ between on-demand and provisioned capacity mode?

**Expected:** Account-level read/write throughput quotas only apply to provisioned capacity mode tables; on-demand mode tables have no account-level throughput quota, only a table-level one.

**System answer:** Based on the provided context:

* **Provisioned capacity mode:** Account-level read and write throughput quotas apply to the sum of the provisioned throughput capacity for all of the account’s tables and global secondary indexes in a given Region (with default quotas of 80,000 read capacity units and 80,000 write capacity units).
* **On-demand capacity mode:** No account-level read and write throughput quotas are applied to tables in on-demand mode (indicated as "Not applicable" in the per-account throughput quota table).

**Grade (fill in correct/incorrect):** 

---

## [c4] (comparison) What's the difference between a local secondary index and a global secondary index in terms of item collection size limits?

**Expected:** A table with one or more local secondary indexes has item collections capped at 10GB because the LSI is colocated in the same partition as the base table; global secondary indexes are independent of the base table and not subject to that same-partition constraint.

**System answer:** Based on the provided context, for a table with one or more local secondary indexes (LSIs), item collections cannot exceed 10GB in size (which includes all base table items and all projected LSI views that share the same partition key attribute value). 

Regarding global secondary indexes (GSIs), the context states that in a GSI, the item collection is independent of the base table and can have a different partition key attribute, but it does not specify a 10GB size limit for GSIs.

**Grade (fill in correct/incorrect):** 

---

## [c5] (comparison) What's the tradeoff between S3 Glacier Instant Retrieval and S3 Glacier Flexible Retrieval?

**Expected:** Glacier Instant Retrieval gives millisecond, real-time access for rarely-accessed data; Glacier Flexible Retrieval is cheaper but data is archived and requires a restore taking minutes to hours before it's accessible.

**System answer:** Based on the provided context, the differences and tradeoff details between the two storage classes are:

* **S3 Glacier Instant Retrieval (GLACIER_IR):** Used for long-term data that is rarely accessed (accessed once a quarter) and requires millisecond retrieval (available for real-time access). It has a minimum storage duration of 90 days, an object size requirement of 128 KB, and per-GB retrieval fees apply.
* **S3 Glacier Flexible Retrieval (GLACIER):** Used for archives where data is accessed less frequently (once a year) and portions might need to be retrieved in minutes to hours. Data is archived and not available for real-time access; you must first restore archived objects before you can access them. It has a minimum storage duration of 90 days, per-GB retrieval fees apply, and it requires 40 KB of additional metadata for each archived object (32 KB charged at the S3 Glacier Flexible Retrieval rate and 8 KB charged at the S3 Standard rate).

**Grade (fill in correct/incorrect):** 

---

## [c6] (comparison) What's the practical difference between EC2's Nitro and Xen hypervisors when choosing an instance type?

**Expected:** Nitro is used by current-generation instance types (e.g. M5, C6i, R7g); Xen is used only by previous-generation instance types (e.g. M1-M4, C1-C4, R3-R4), so Nitro is what you'd pick for anything modern.

**System answer:** Based on the provided context, there is no mention of the practical differences between Nitro and Xen hypervisors when choosing an instance type. The context only lists which instance types use Nitro and which use Xen.

**Grade (fill in correct/incorrect):** 

---

## [o1] (operational) I tagged an S3 object to trigger a lifecycle transition, but now I want to cancel it before it runs. What should I do?

**Expected:** Remove the tag rather than disabling the rule, since rule policy updates can take up to 15 minutes to propagate; even then, cancellation isn't guaranteed because evaluation and execution timing aren't deterministic.

**System answer:** Based on the context, if you need to prevent a transition before it executes, you should remove the tag rather than disabling the rule (as rule policy updates can take up to 15 minutes to propagate). 

However, because the time between evaluation and execution is not deterministic, removing a tag does not guarantee an immediate cancellation. To reliably prevent a transition after tagging an object, you should wait for a Lifecycle Event Notification confirming the action completed before removing the tag.

**Grade (fill in correct/incorrect):** 

---

## [o2] (operational) How should I restrict SSH access to my EC2 instance using security groups?

**Expected:** Add an inbound rule for port 22 that authorizes only specific IP address ranges — do not use 0.0.0.0/0 (or ::/0 for IPv6), which would allow access from any IP address.

**System answer:** Based on the provided context, to restrict SSH access to your EC2 instances using security groups, you should:

* Authorize only specific IP address ranges for inbound rules on port 22 (SSH), rather than specifying 0.0.0.0/0 (IPv4) or ::/ (IPv6).
* Ensure that access through port 22 is restricted to the sources or destinations that require it. 
* Restrict inbound traffic to authorized sources, such as the ID of an instance security group, the ID of an endpoint security group, or specific IPv4/IPv6 address ranges (like the VPC IPv4 or IPv6 CIDR, depending on your setup and whether client IP preservation is on or off).

**Grade (fill in correct/incorrect):** 

---

## [o3] (operational) How do I move an object out of S3 Glacier Deep Archive back to S3 Standard?

**Expected:** You can't do it with a Lifecycle rule directly — Glacier Deep Archive transitions only go one way. You must first restore a temporary copy of the object, then use a copy operation to overwrite it specifying S3 Standard as the destination storage class.

**System answer:** Based on the provided context, to change the storage class of an object from S3 Glacier Deep Archive to another storage class (such as S3 Standard):

1. You must first use the restore operation to make a temporary copy of the object.
2. Then, use the copy operation to overwrite the object, specifying S3 Standard as the storage class. 

*(Note: For objects in the S3 Glacier Deep Archive storage class, the Copy operation for restored objects is not supported in the Amazon S3 console, so you must use the AWS Command Line Interface (AWS CLI), the AWS SDKs, or the REST API.)*

**Grade (fill in correct/incorrect):** 

---

## [o4] (operational) My DynamoDB BatchWriteItem call includes 30 PutItem requests. Will it succeed?

**Expected:** No — a single BatchWriteItem operation can contain at most 25 PutItem or DeleteItem requests, so 30 requests exceeds the limit.

**System answer:** Based on the provided context, the answer is no. A single BatchWriteItem operation can contain up to 25 PutItem or DeleteItem requests (and writes up to 25 items to one or more tables), whereas your call includes 30 PutItem requests.

**Grade (fill in correct/incorrect):** 

---

## [o5] (operational) How many times per day can I decrease provisioned throughput on a DynamoDB table?

**Expected:** You start each day (UTC) with 4 available decreases, plus 1 more becomes available each hour up to a max of 4 available at any time — allowing up to 27 decreases over a full 24-hour day.

**System answer:** Over a full 24-hour day, you can decrease provisioned throughput on a DynamoDB table up to 27 times.

**Grade (fill in correct/incorrect):** 

---

## [o6] (operational) I need more than 2,500 DynamoDB tables in one AWS account/region. What are my options?

**Expected:** You can contact your AWS account team to request an increase up to a maximum of 10,000 tables per account/region; beyond 10,000, the recommended practice is to use multiple accounts.

**System answer:** Based on the provided context, your options are:

1. Reach out to your AWS account team to explore an increase up to a maximum of 10,000 tables.
2. If you need more than 10,000 tables, the recommended best practice is to set up multiple accounts, each of which can serve up to 10,000 tables.

**Grade (fill in correct/incorrect):** 

---
