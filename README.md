# CloudFriend3

CloudFriend3 is an asynchronous cloud intelligence and governance platform designed to help engineering teams monitor AWS infrastructure, detect underutilized resources, estimate cloud cost, track historical trends, and improve cloud visibility.

It combines infrastructure scanning, metrics analysis, pricing estimation, trend analytics, background workers, scheduling, Slack notifications, and API reporting into one unified platform.

---

# Project Vision

CloudFriend3 solves a real-world cloud problem:

> Teams launch infrastructure, but over time lose visibility into utilization, ownership, and cost.

CloudFriend3 acts as a cloud intelligence layer that continuously evaluates infrastructure and provides explainable insights.

---

# Core Features

## AWS Infrastructure Discovery

Scans AWS infrastructure using configured credentials.

Collects:

* EC2 inventory
* Regions
* Tags
* Metadata
* Instance age

---

## CloudWatch Metrics Analysis

Reads AWS CloudWatch metrics to analyze utilization.

Tracks:

* CPU utilization
* Activity levels
* Resource behavior over time

---

## Cost Estimation Engine

Estimates monthly cloud cost based on instance type.

Example:

```text
t3.micro → ~$9/month
```

---

## Risk Engine

Assigns risk levels to infrastructure.

### Risk Levels

* High
* Medium
* Low
* New

Risk is determined using:

* CPU utilization
* Resource age
* Monthly cost
* Historical trends
* Ownership metadata

---

## Trend Analytics

Stores previous scans and compares historical behavior.

Trend examples:

* Stable
* Increasing Cost
* Decreasing Cost
* No History

---

## Queue + Worker Architecture

CloudFriend3 uses asynchronous processing.

Workflow:

```text
CLI / Scheduler
        ↓
Redis Queue
        ↓
RQ Worker
        ↓
AWS Scan
        ↓
Analysis
        ↓
Report
```

Benefits:

* Non-blocking scans
* Scalable execution
* Production-friendly design

---

## PostgreSQL Persistence

Stores scan history.

Useful for:

* Trend analysis
* Historical comparison
* Reporting

---

## Slack Notifications

Sends alerts for high-risk infrastructure.

Example:

```text
High-risk resource detected
CPU below threshold
Potential waste found
```

---

## Scheduler Automation

Runs periodic scans automatically.

Powered by:

* APScheduler

Example:

```text
Daily 9 AM scan
```

---

## API Layer

Provides access to reports.

Built using FastAPI.

Example:

```text
/report
```

---

# Workflow Architecture

```text
Scheduler / CLI Trigger
            ↓
      Redis Queue
            ↓
        RQ Worker
            ↓
     AWS Infrastructure
            ↓
 CloudWatch Metrics + Tags
            ↓
      Pricing Engine
            ↓
      Trend Analytics
            ↓
         Risk Engine
            ↓
     PostgreSQL Storage
            ↓
    Reports / API / Slack
```

---

# Folder Structure

```text
cloudfriend3/
│
├── analytics/
├── analyzer/
├── alerts/
├── api/
├── cli/
├── collectors/
├── jobqueue/
├── metrics/
├── pricing/
├── reports/
├── scheduler/
├── storage/
├── requirements.txt
└── README.md
```

---

# Installation

## Clone Repository

```bash
git clone YOUR_REPO_URL
cd cloudfriend3
```

---

## Create Virtual Environment

Linux / Mac:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# AWS Configuration

Configure AWS credentials:

```bash
aws configure
```

Verify:

```bash
aws sts get-caller-identity
```

---

# Running CloudFriend3

## Start Redis

Linux:

```bash
sudo service redis-server start
```

Check:

```bash
redis-cli ping
```

Expected:

```text
PONG
```

---

## Start Worker

```bash
rq worker
```

---

## Run Scan

```bash
python3 -m cli.main scan
```

---

## Explain Resource

```bash
python3 -m cli.main explain INSTANCE_ID
```

Example:

```bash
python3 -m cli.main explain i-053dd1dfa96e90402
```

---

## Start API

```bash
uvicorn api.server:app --reload
```

Open:

```text
http://127.0.0.1:8000/report
```

---

## Run Scheduler

```bash
python3 -m scheduler.daily_scan
```

---

# Example Output

```json
[
  {
    "instance_id": "i-053dd1dfa96e90402",
    "name": "jenkins",
    "cpu_avg": 0.14,
    "monthly_cost": 9,
    "trend": "Stable",
    "risk": "High"
  }
]
```

---

# Example CLI Report

```text
CloudFriend3 Infrastructure Intelligence Report

Instance Name      CPU Avg     Cost     Risk
-------------------------------------------------
jenkins             0.14%       $9       High
backend-api         37.20%      $42      Low
analytics-worker    2.31%       $18      Medium
```

---

# Tech Stack

* Python
* AWS
* CloudWatch
* Redis
* RQ Workers
* PostgreSQL
* FastAPI
* APScheduler
* SQLAlchemy

---

# Real-World Problems Solved

CloudFriend3 helps solve:

* Idle cloud infrastructure
* Hidden cloud cost
* Missing ownership
* Manual cloud audits
* Lack of historical visibility
* Delayed engineering awareness

---

# Similar Industry Tools

CloudFriend3 belongs to the same category as:

* CloudHealth
* Cloud Custodian
* Komiser
* Infracost
* CloudQuery
* OpenCost

---

# Use Cases

* DevOps cloud audits
* Cost optimization
* Platform engineering
* Cloud governance
* Internal cloud monitoring
* Engineering visibility

---

# Future Roadmap

Potential upgrades:

* Multi-account AssumeRole scanning
* Dashboard UI
* Kubernetes support
* RDS/EBS/Lambda analysis
* Live AWS pricing API
* Advanced anomaly detection

---

# Project Summary

CloudFriend3 is an asynchronous cloud intelligence platform that scans AWS infrastructure, analyzes CloudWatch metrics, estimates cloud cost, tracks historical trends, assigns explainable risk scores, stores insights in PostgreSQL, triggers Slack alerts, supports scheduled scans, exposes APIs, and helps engineering teams improve cloud governance and infrastructure visibility.
