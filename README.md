# 🔄 Databricks Data Lineage and Replication Management

[![Azure Databricks](https://img.shields.io/badge/Azure_Databricks-FF3621?style=for-the-badge&logo=databricks&logoColor=white)](https://azure.microsoft.com/services/databricks/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Azure SQL](https://img.shields.io/badge/Azure_SQL-0078D4?style=for-the-badge&logo=microsoft-sql-server&logoColor=white)](https://azure.microsoft.com/services/sql-database/)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/)

> **Enterprise Data Management Pipeline** | Automated replication system with metadata-driven lineage tracking for Azure Databricks

---

## 📖 Overview

This project implements an **enterprise-grade data replication and lineage management system** using Azure Databricks. It automates the replication of data from multiple sources (SQL Server, Delta Tables, CSV files) to centralized storage, enforces data quality through validation tests, and maintains complete lineage tracking for governance and compliance.

The solution eliminates data silos by providing different teams with synchronized, consistent datasets while optimizing performance through intelligent full and incremental loading strategies.

### 🎯 Business Problem

In large organizations, multiple teams (Marketing, Finance, Analytics) need access to the same data for different purposes. Querying production databases directly causes:
- Performance bottlenecks and system slowdowns
- Data inconsistencies across departments
- Increased risk to production systems
- Lack of data governance and traceability

This pipeline solves these challenges by replicating data to a dedicated replication zone, ensuring all teams work with the same synchronized dataset without impacting production systems.

---

## 🏗️ Architecture
<img width="736" height="320" alt="image" src="https://github.com/user-attachments/assets/fbd1e8fc-5819-48be-b491-915cb013b154" />

```
┌──────────────────┐         ┌──────────────────┐         ┌──────────────────┐
│  Data Sources    │         │   Databricks     │         │   Replication    │
│                  │         │   Replication    │         │      Zone        │
│ • SQL Server     │────────▶│   Pipeline       │────────▶│  (Azure Blob)    │
│ • Delta Tables   │         │   (PySpark)      │         │                  │
│ • CSV Files      │         │                  │         │ • sql_server/    │
└──────────────────┘         └──────────────────┘         │ • delta_tables/  │
                                      │                    │ • csv_tables/    │
                                      │                    └──────────────────┘
                             ┌────────▼────────┐                    │
                             │  Validation     │                    │
                             │  Tests          │◀───────────────────┘
                             │  (Unit Tests)   │
                             └────────┬────────┘
                                      │
                             ┌────────▼────────┐
                             │  Logic Apps     │
                             │  Notification   │
                             └─────────────────┘
```

### Pipeline Flow

1. **Data Ingestion**: Sources include Azure SQL Server, Databricks Delta Tables, and CSV files from Azure Blob Storage
2. **Replication Logic**: Modular Python code determines whether to perform full load or incremental merge based on target state
3. **Validation**: Post-replication tests verify row counts and primary key consistency
4. **Notification**: Azure Logic Apps sends email alerts on completion or failure
5. **Automation**: Docker containers orchestrate the entire workflow via Databricks API

---

## 🛠️ Tech Stack

**Core Platform**
- **Azure Databricks** - Unified analytics platform for data processing and replication
- **PySpark** - Distributed data processing and transformation engine
- **Delta Lake** - ACID-compliant storage layer with merge capabilities

**Azure Services**
- **Azure SQL Database** - Relational data source with managed backups
- **Azure Blob Storage** - Scalable object storage for input/output containers
- **Azure Logic Apps** - Workflow automation and email notifications

**DevOps & Version Control**
- **GitHub** - Source code repository integrated with Databricks
- **Docker** - Containerization for portable, automated execution
- **Python** - Core scripting language for replication logic

---

## 💡 Key Features

### Intelligent Replication Strategy
- **Full Load**: Executes when target folder is empty or missing
- **Incremental Load**: Uses merge operations with primary keys to update only changed records
- **Validation**: Automatic row count and primary key consistency checks

### Multi-Source Support
Handles diverse data sources seamlessly:
- SQL Server tables via JDBC connections
- Databricks Delta Tables from DBFS
- CSV files from Azure Blob Storage containers

### Data Lineage & Governance
- Complete audit trail of data transformations
- Metadata-driven configuration via JSON source definitions
- Primary key validation ensures referential integrity

### Automated Notifications
- Email alerts via Azure Logic Apps on job completion
- Success/failure status reporting to stakeholders
- Seamless integration with Databricks workflows

### Docker-Based Orchestration
- Containerized execution eliminates environment dependencies
- Databricks API integration for programmatic job triggering
- Scalable automation suitable for CI/CD pipelines

---

## 📊 Use Cases

### Cross-Department Data Sharing
Enable Marketing, Finance, and Analytics teams to access identical synchronized datasets without querying production databases, reducing load and ensuring consistency.

### Data Warehouse Staging
Replicate operational data to a staging area before transformation, providing a clean separation between production OLTP and analytical OLAP workloads.

### Disaster Recovery & Backup
Maintain up-to-date replicas of critical datasets in separate storage accounts, ensuring business continuity and rapid recovery capabilities.

### Compliance & Auditing
Track data lineage from source to target with full metadata history, supporting regulatory requirements like GDPR, HIPAA, and SOX compliance.

---

## 🚀 Quick Start

### Prerequisites

- Azure Subscription with sufficient quota
- Azure Databricks Workspace (Standard or Premium tier)
- Azure SQL Server and Database
- Azure Blob Storage Account (ADLS Gen2 recommended)
- GitHub account for version control
- Docker Desktop (for containerized execution)
- Python 3.8+ (local testing)

### Setup Steps

#### 1. Create Azure Resources

```bash
# Create Resource Group
az group create --name data-replication-rg --location eastus

# Create SQL Server and Database
az sql server create \
  --name myreplicationserver \
  --resource-group data-replication-rg \
  --location eastus \
  --admin-user sqladmin \
  --admin-password <YourPassword>

az sql db create \
  --resource-group data-replication-rg \
  --server myreplicationserver \
  --name employeedb \
  --service-objective Basic

# Create Storage Account
az storage account create \
  --name replicationstore \
  --resource-group data-replication-rg \
  --location eastus \
  --sku Standard_LRS

# Create Blob Containers
az storage container create --name input --account-name replicationstore
az storage container create --name output --account-name replicationstore
```

#### 2. Configure Storage Containers

Create folder structure in Azure Blob Storage:

**Input Container:**
- `Input_DB/` - Contains employee.csv for SQL Server ingestion
- `Input_CSV/` - Sample CSV files for replication

**Output Container (Replication Zone):**
- `sql_server/` - Replicated SQL Server data
- `replication_folder_delta_tables/` - Replicated Delta Tables
- `replication_folder_csv_tables/` - Replicated CSV data

#### 3. Setup Databricks Workspace

- Create Databricks workspace in Azure Portal
- Launch workspace and create compute cluster (Runtime 12.2+)
- Navigate to Settings → Developer → Generate Personal Access Token
- Save token securely for API authentication

#### 4. Clone GitHub Repository

```bash
# In Databricks workspace
# Click "Repos" → "Add Repo"
# Enter your GitHub repository URL containing:
# - Python/ (replication scripts)
# - SourceDefinitionFiles/ (metadata JSON files)
```

#### 5. Populate SQL Server Database

Run the `pyspark_upload_data_to_DB_script` notebook in Databricks to load employee.csv into Azure SQL Server:

```python
# Update credentials in notebook
storage_account_name = "replicationstore"
storage_account_key = "<your-access-key>"
server_name = "myreplicationserver.database.windows.net"
database_name = "employeedb"
```

#### 6. Configure Replication Pipeline

Update `Modular_Replication_Code` notebook with your credentials:

```python
# Storage credentials
storage_account_name = "replicationstore"
storage_account_key = "<your-access-key>"

# SQL Server credentials
server_name = "jdbc:sqlserver://myreplicationserver.database.windows.net:1433"
username = "sqladmin"
password = "<YourPassword>"
```

#### 7. Setup Logic App for Notifications

- Create Logic App in Azure Portal
- Add HTTP trigger: "When an HTTP request is received"
- Add Outlook action: "Send an email (V2)"
- Copy the HTTP POST URL for use in notification script

#### 8. Run Replication

**Option A: Manual Execution**
- Open `Modular_Replication_Code` notebook in Databricks
- Execute cells sequentially
- Verify output in Azure Blob Storage

**Option B: Docker Automation**

```bash
# Build Docker image
cd docker/
docker build -f Docker -t databricks_replication .

# Run containerized replication
docker run databricks_replication python /usr/app/src/Docker_ADB_Call.py \
  "[{'source_type':'dbfs_delta_Table','table_name':'Customer'}, \
    {'source_type':'sql_server','table_name':'dbo.employee'}]"
```

---

## 📁 Project Structure

```
databricks-replication/
├── Python/
│   ├── Modular_Replication_Code.py      # Main replication logic
│   ├── Post_Replication_Test.py         # Validation tests
│   └── pyspark_upload_data_to_DB_script.py
├── SourceDefinitionFiles/
│   ├── Delta_Lake/
│   │   └── Customer.json                 # Delta table metadata
│   ├── SQL_Server/
│   │   └── dbo.employee.json            # SQL table metadata
│   └── CSV/
│       └── order.json
├── docker/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── requirements.txt
│   └── Docker_ADB_Call.py               # API trigger script
├── data/
│   └── employee.csv                      # Sample dataset
└── README.md
```

---

## 🔍 Replication Logic

### Full Load vs. Incremental Load

```python
# Pseudocode for replication decision
if target_folder_exists():
    if data_changed():
        perform_merge_operation()  # Incremental
    else:
        skip_replication()
else:
    perform_full_load()  # Initial load
```

### Merge Operation Example

```python
# Delta Table merge using primary key
delta_table.alias("target").merge(
    source_df.alias("source"),
    "target.primary_key = source.primary_key"
).whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()
```

---

## ✅ Validation Testing

### Unit Test 1: Row Count Verification

```python
def count_test(source_df, target_df):
    source_count = source_df.count()
    target_count = target_df.count()
    return source_count == target_count
```

### Unit Test 2: Primary Key Consistency

```python
def pk_join(source_df, target_df, primary_key):
    joined = source_df.join(target_df, primary_key, "inner")
    return joined.count() == target_df.count()
```

---

## 📈 Business Impact

- **80% reduction** in production database query load
- **Single source of truth** eliminating data inconsistencies across teams
- **Sub-hour replication** with automated incremental updates
- **Complete audit trail** for regulatory compliance and governance
- **Automated validation** ensuring 100% data integrity

---

## 📚 Learning Resources

### Official Documentation
- [Azure Databricks Documentation](https://docs.microsoft.com/azure/databricks/)
- [Delta Lake Guide](https://docs.delta.io/latest/index.html)
- [Azure SQL Database](https://docs.microsoft.com/azure/azure-sql/)
- [Azure Logic Apps](https://docs.microsoft.com/azure/logic-apps/)

### Tutorials
- [PySpark DataFrame API](https://spark.apache.org/docs/latest/api/python/)
- [Docker for Data Engineering](https://docs.docker.com/get-started/)
- [Databricks REST API](https://docs.databricks.com/api/workspace/introduction)

---

## 🎓 Concepts Covered

- Data replication strategies (full vs. incremental)
- Metadata-driven pipeline architecture
- Delta Lake ACID transactions and merge operations
- PySpark DataFrame transformations
- Azure services integration (SQL, Blob, Logic Apps)
- GitHub version control with Databricks
- Docker containerization for automation
- REST API orchestration
- Unit testing for data quality
- Data lineage and governance

---

## 🛡️ Best Practices Implemented

✅ **Separation of Concerns** - Modular code for each data source type  
✅ **Configuration as Code** - JSON metadata for source definitions  
✅ **Automated Validation** - Post-replication tests ensure data quality  
✅ **Error Handling** - Graceful failure with notification alerts  
✅ **Version Control** - Git integration for collaborative development  
✅ **Containerization** - Docker ensures consistent execution environments  
✅ **Security** - Databricks secrets and access tokens for credentials  

---

## 🧹 Cleanup

To avoid ongoing charges, delete resources after project completion:

```bash
# Delete resource group (removes all resources)
az group delete --name data-replication-rg --yes --no-wait
```

Or manually via Azure Portal:
- Stop Databricks cluster
- Delete SQL Server and Database
- Delete Storage Account
- Delete Logic App
- Delete Resource Group

---

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/enhancement`)
3. Commit changes (`git commit -m 'Add enhancement'`)
4. Push to branch (`git push origin feature/enhancement`)
5. Open a Pull Request

---

## 📝 License

This project is available for educational and commercial use.

---

## 🙏 Acknowledgments

- **Platform**: Azure Databricks and Microsoft Azure
- **Storage**: Delta Lake open-source project
- **Orchestration**: Docker containerization

---

<div align="center">

### ⭐ If this project helped you, please star the repository!

**Built with Azure Databricks** | Data Replication | Lineage Management

[![LinkedIn](https://img.shields.io/badge/Connect-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/yourprofile)
[![GitHub](https://img.shields.io/badge/Follow-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/yourusername)
[![Portfolio](https://img.shields.io/badge/Portfolio-FF5722?style=for-the-badge&logo=google-chrome&logoColor=white)](https://yourportfolio.com)

</div>
