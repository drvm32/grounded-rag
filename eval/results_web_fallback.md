# Unanswerable question eval results

## [u1] What is the price per GB-month for S3 Standard storage in the us-east-1 region?

**Expected:** Not answerable from this corpus — pricing figures aren't included in the ingested docs, which only reference a separate pricing page.

**System answer:** The price per GB-month for S3 Standard storage in the us-east-1 region for the first 50 TB is $0.023 [https://www.cloudzero.com/blog/s3-pricing, https://cloudburn.io/blog/amazon-s3-pricing, https://aws.amazon.com/s3/pricing]. For additional volumes, the price is $0.022 per GB for the next 450 TB, and $0.021 per GB for storage over 500 TB [https://cloudburn.io/blog/amazon-s3-pricing, https://aws.amazon.com/s3/pricing].

**Grade (fill in correct refusal/incorrect - hallucinated):** 

---

## [u2] How do I configure an EC2 Auto Scaling Group to scale based on CPU utilization?

**Expected:** Not answerable from this corpus — Auto Scaling isn't covered by any ingested document.

**System answer:** To configure an EC2 Auto Scaling group to scale based on CPU utilization, follow these steps using the target tracking scaling policy:

1. **Set Group Size:** Define your minimum and maximum capacities in the Group size box (for example, setting a minimum capacity of 2 and a maximum of 5) [https://johnnymaclean.medium.com/how-to-use-amazon-ec2-auto-scaling-372989386b38].
2. **Configure Scaling Policies:** 
   - Select the **Target tracking scaling policy** [https://johnnymaclean.medium.com/how-to-use-amazon-ec2-auto-scaling-372989386b38].
   - Set the **Metric type** to **Average CPU utilization** [https://johnnymaclean.medium.com/how-to-use-amazon-ec2-auto-scaling-372989386b38].
   - Ensure the **Target value** is set (for example, to 50) [https://johnnymaclean.medium.com/how-to-use-amazon-ec2-auto-scaling-372989386b38, https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-scaling-target-tracking.html]. 
3. **Additional Recommendations:** 
   - Enable detailed monitoring for Amazon EC2 metrics so that CPU utilization is published at one-minute intervals (instead of the default five-minute intervals) to allow the policy to detect and respond faster to changes [https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-scaling-target-tracking.html].

**Grade (fill in correct refusal/incorrect - hallucinated):** 

---

## [u3] Can a DynamoDB Stream trigger an AWS Lambda function, and if so, how many concurrent executions are allowed?

**Expected:** Not answerable from this corpus — Lambda integration isn't covered by any ingested document.

**System answer:** Yes, a DynamoDB Stream can trigger an AWS Lambda function [https://www.capitalone.com/tech/software-engineering/dynamodb-streams-lambda-pattern-best-practices, https://aws.amazon.com/blogs/database/build-scalable-event-driven-architectures-with-amazon-dynamodb-and-aws-lambda]. 

Regarding the number of concurrent executions allowed:
* **Shard mapping:** Each shard in DynamoDB Streams maps to a single Lambda instance, and each Lambda invocation is triggered on a per-shard basis [https://www.capitalone.com/tech/software-engineering/dynamodb-streams-lambda-pattern-best-practices]. 
* **Parallelization Factor:** You can configure the `ParallelizationFactor` setting (ranging from 1 to 10) to allow multiple Lambda instances to process a single DynamoDB stream shard concurrently [https://aws.amazon.com/blogs/database/build-scalable-event-driven-architectures-with-amazon-dynamodb-and-aws-lambda].
* **Limits:** Lambda executions are ultimately subject to concurrency limits at both the individual function and account levels [https://www.capitalone.com/tech/software-engineering/dynamodb-streams-lambda-pattern-best-practices].

**Grade (fill in correct refusal/incorrect - hallucinated):** 

---

## [u4] How does Multi-AZ failover work for an Amazon RDS database instance?

**Expected:** Not answerable from this corpus — RDS is a different AWS service not covered by any ingested document.

**System answer:** Based on the provided context, Multi-AZ failover works as follows:

* **Triggering a Failover:** If the primary DB instance experiences issues with network connectivity, compute unit failure, storage failure, or an unplanned service disruption, Amazon RDS automatically detects the failure [https://aws.amazon.com/blogs/database/using-rds-proxy-with-amazon-rds-multi-az-db-instance-deployment-to-improve-planned-failover-time, https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_SQLServerMultiAZ.html]. 
* **Planned vs. Unplanned:** Failovers can be planned (such as during maintenance operations like instance class modifications and OS upgrades once the standby catches up) or unplanned (due to service disruptions) [https://aws.amazon.com/blogs/database/using-rds-proxy-with-amazon-rds-multi-az-db-instance-deployment-to-improve-planned-failover-time, https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_SQLServerMultiAZ.html].
* **Promotion and Endpoint Transition:** RDS automatically promotes the up-to-date standby/secondary instance to the primary role [https://aws.amazon.com/blogs/database/using-rds-proxy-with-amazon-rds-multi-az-db-instance-deployment-to-improve-planned-failover-time, https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_SQLServerMultiAZ.html]. The physical network address of the shared endpoint transitions to the secondary replica, allowing database operations to resume quickly without requiring application reconfiguration or manual intervention [https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_SQLServerMultiAZ.html]. This failover process is typically completed within 60-120 seconds [https://repost.aws/questions/QU4DYhqh2yQGGmjE_x0ylBYg/what-happens-after-failover-in-rds].
* **After Failover:** The failed primary instance is brought back up as the new standby instance to reinstate high-availability, and storage-level replication is resumed [https://aws.amazon.com/blogs/database/using-rds-proxy-with-amazon-rds-multi-az-db-instance-deployment-to-improve-planned-failover-time, https://repost.aws/questions/QU4DYhqh2yQGGmjE_x0ylBYg/what-happens-after-failover-in-rds].

**Grade (fill in correct refusal/incorrect - hallucinated):** 

---

## [u5] What SLA uptime percentage does AWS guarantee for EC2 instances?

**Expected:** Not answerable from this corpus — SLA terms aren't covered by any ingested document.

**System answer:** Based on the provided context, AWS guarantees different SLA uptime percentages for EC2 instances depending on the deployment architecture:

* **Multi-AZ (deploying instances across at least two Availability Zones in the same region / 2+ instances):** Guarantees **99.99%** uptime [https://hykell.com/knowledge-base/aws-performance-sla, https://www.dev-toolbox.tech/tools/uptime-calculator/examples/aws-ec2-sla].
* **Single Instance:** Guarantees **99.5%** availability (Instance-Level SLA) [https://hykell.com/knowledge-base/aws-performance-sla, https://aws.amazon.com/compute/sla/historical].

**Grade (fill in correct refusal/incorrect - hallucinated):** 

---

## [u6] How do I set up a cross-account IAM role to let another AWS account access my S3 bucket?

**Expected:** Not answerable from this corpus — cross-account IAM role configuration isn't covered by any ingested document.

**System answer:** To set up cross-account IAM roles to manage S3 bucket access, you can follow the steps outlined below:

**Method 1 (Using Account A to assume a role in Account B):**
1. **Create a Role in Account B:** Go to the IAM console in Account B, create a new role, and select "Another AWS Account" as the trusted entity. Enter Account A's ID as the trusted account and attach an appropriate policy that grants access to the S3 bucket (such as `s3:ListBucket` and `s3:GetObject`) [https://medium.com/@slava.rudnev/aws-services-s3-cross-account-access-management-using-bucket-policies-and-iam-d8e1149edd9f].
2. **Set up Permissions in Account A:** In Account A, set up permissions (via an IAM policy) for a user or application to assume the role created in Account B using the `sts:AssumeRole` action [https://medium.com/@slava.rudnev/aws-services-s3-cross-account-access-management-using-bucket-policies-and-iam-d8e1149edd9f].
3. **Configure Account B's Bucket Policy:** Edit and save the bucket policy in Account B's S3 console to grant the necessary permissions to the trusted principal or account [https://medium.com/@slava.rudnev/aws-services-s3-cross-account-access-management-using-bucket-policies-and-iam-d8e1149edd9f].

**Method 2 (Using Account A to manage access for Account B):**
1. **Create an IAM Role in Account A:** Create an IAM role in Account A that can be assumed by users or roles from Account B [https://repost.aws/knowledge-center/cross-account-access-s3].
2. **Grant Role Permissions and Trust Policy:** Grant the role permissions to perform the required S3 operations. In the role's trust policy, grant a user or role from Account B permissions to assume the role in Account A using a trust policy that defines the principal (e.g., `"Action": "sts:AssumeRole"`) [https://repost.aws/knowledge-center/cross-account-access-s3].
3. **Configure Account B and Buckets:** Create an IAM user or role in Account B with permissions to perform required S3 operations (such as `PutObject` and `GetObject`), and configure the bucket ACL or bucket policy to include permissions for Account B [https://repost.aws/knowledge-center/cross-account-access-s3].

**Grade (fill in correct refusal/incorrect - hallucinated):** 

---
