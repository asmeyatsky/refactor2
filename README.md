# CMAS - Cloud Migration Agent Suite

**CMAS** is an intelligent, agentic framework designed to automate the migration of legacy AWS infrastructure code (Python/Boto3 and Terraform) to Google Cloud Platform (GCP).

It leverages a multi-agent architecture to not only translate code but also validate its correctness through synthesized tests, ensuring a reliable migration path.

## 🚀 Key Features

*   **Multi-Agent Architecture**:
    *   **Refactor Agent**: Analyzes AWS code and intelligently translates it to GCP equivalents using a plugin-based mapping system.
    *   **Validation Agent**: Synthesizes unit tests for the migrated code to verify functional correctness and detects incomplete translations.
*   **Comprehensive Service Support**: Supports migration for over 15 major AWS services including S3, SNS, SQS, DynamoDB, Lambda, EC2, and more.
*   **Modern Agentic Dashboard**: A sleek, dark-mode web UI for real-time interaction, visualizing agent thought processes, and comparing source vs. migrated code side-by-side.
*   **Smart Validation**: Automatically detects untranslated SDK calls (e.g., leftover `boto3` references) and flags them with precise line numbers.
*   **Extensible Plugin System**: Service mappings are defined in JSON, making it easy to add support for new services without changing core logic.

## 🛠️ Supported Mappings

CMAS currently supports the following AWS to GCP migrations:

| AWS Service | GCP Equivalent | Status |
| :--- | :--- | :--- |
| **S3** | Cloud Storage | ✅ Full Support |
| **SNS** | Pub/Sub (Topics) | ✅ Full Support |
| **SQS** | Pub/Sub (Subscriptions) | ✅ Full Support |
| **DynamoDB** | Firestore | ✅ Full Support |
| **Lambda** | Cloud Functions | ✅ Full Support |
| **Kinesis** | Pub/Sub | ✅ Full Support |
| **Redshift** | BigQuery | ✅ Full Support |
| **ECS/Fargate** | Cloud Run | ✅ Full Support |
| **EKS** | GKE | ✅ Full Support |
| **Route53** | Cloud DNS | ✅ Full Support |
| **ElastiCache** | Memorystore (Redis) | ✅ Full Support |
| **CloudWatch** | Cloud Monitoring | ✅ Full Support |
| **IAM** | Cloud IAM | ✅ Full Support |
| **Glue** | Dataflow | ✅ Full Support |

## 🏗️ Architecture

The project is organized into the following components:

```
cmas/
├── refactor_agent/       # Logic for code translation
│   └── src/translate.py  # Regex and AST-based translation engine
├── validation_agent/     # Logic for test synthesis and verification
│   └── src/synthesize.py # Generates tests to validate migrated code
├── services/             # JSON definitions for Service Mappings
├── ui/                   # Web Dashboard (Flask + Vanilla JS/CSS)
│   ├── static/           # Frontend assets (Modern Dark Theme)
│   └── server.py         # Backend API
└── framework/            # Shared utilities and plugin manager
```

## 💻 Getting Started

### Prerequisites
*   Python 3.8+
*   `pip`

### Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/your-repo/cmas.git
    cd cmas
    ```

2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Running the Dashboard

1.  Start the UI server:
    ```bash
    python3 cmas/ui/server.py
    ```

2.  Open your browser and navigate to:
    `http://127.0.0.1:8000`

## 📖 Usage

1.  **Paste Code**: Copy your AWS Python (Boto3) or Terraform code into the **Left Panel**.
2.  **Migrate**: Click the **MIGRATE & VALIDATE** button.
3.  **Observe**: Watch the **Active Agents** analyze and process your code in real-time.
4.  **Review**:
    *   **Right Panel**: View the generated GCP code.
    *   **Status**: Check the validation result (Success/Fail).
    *   **Logs**: Monitor detailed system logs in the bottom terminal.
5.  **Copy**: Use the **COPY CODE** button to use your new GCP code.

## 🛡️ Validation Logic

The Validation Agent performs strict checks:
1.  **Import Verification**: Ensures the generated code can be imported.
2.  **SDK cleanup**: Scans for any remaining `boto3` or `botocore` references. If found, validation **FAILS** and reports the exact line number of the untranslated code.

## 🎨 UI Theme

The dashboard features a custom **"Developer Dark"** theme designed for long coding sessions, featuring:
*   Zinc/Slate color palette.
*   Inter & JetBrains Mono typography.
*   Split-view layout for efficient diffing.
*   Live status indicators.

---
*Built with ❤️ by the CMAS Team*
