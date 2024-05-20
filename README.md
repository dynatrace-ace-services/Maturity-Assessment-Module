# Maturity-Health-Script
Maturity Assessment Automation Script
This user manual outlines the utilization of a Python script designed for the automation of maturity assessment on a Dynatrace tenant. The script leverages various Dynatrace APIs with specified scopes, requiring users to generate API tokens for access. The manual covers installation, configuration, execution, and interpretation of results, addressing prerequisites, troubleshooting, and best practices. With a focus on clarity, it provides direct guidance for API token generation and usage, along with support and contact information. The document aims to assist system administrators, Dynatrace users, and IT managers in effectively implementing the maturity assessment automation script

## Purpose
This script assesses Dynatrace maturity levels using specified APIs.

## Audience
System administrators, Dynatrace users, and IT managers.

## Prerequisites
Dynatrace Account: SAAS/Managed tenant URL with API path.
 
## API Tokens:
### API v2 Scopes
	settings.read, releases.read, events.read, problems.read, metrics.read, securityProblems.read, attacks.read

### API v1 Scopes
	ReadConfig, oneAgents.read, ReadSyntheticData

### PaaS Scopes
	PaaS integration - Installer download PaaS integration - Support alert

### Dynatrace Modules Scopes
	Dynatrace module integration - Synthetic Classic

## Getting Started
1. Install Python on the Server
2. Download Python:
	Visit Python's official website and download the latest version compatible with your server's operating system.
3. Install Python:
	Follow the installation instructions provided on the Python website to install Python on your server.
	Verify Installation:
	Open a terminal or command prompt and run the following command to verify the installation:
	python --version

## Execute Python Maturity Assessment Script
1. Download the Python Maturity Assessment project scripts residing inside the sourcecode dir.
	maturityScript.py, utils.py, config.json
2. Using the terminal or command prompt, navigate to the directory where the files are present, update the values inside the config.json file:
	fill in the necessary values such as Tenant Address, API tokens, Filename, and Account-Uuid.
3. Verify API Connectivity:
	Run a test script or command to verify API connectivity. For example:
	curl -kv https://api-url
4. Locate the template files "MaturityScript_automation_template.xlsx" from the sharepoint link -  [MaturityScript_automation_template.xlsx](https://dynatrace-my.sharepoint.com/:x:/p/nicolas_vailliet/EdxCK9e_rA1MnHT6Oxs6ICEBu6oQ477SqbBlhWZI4crsGw?e=aeqrYd)
5. Place the above template files inside the dir where the maturityScript.py is present.
	MaturityScript_automation_template.xlsx - Input template file
6. Edit the config.json file to include tenant address, token and account UUID.
7. Execute Maturity Assessment Script:
	Run the maturity assessment script using the following command:
	python maturityScript.py

## Review Results
After script execution, review the generated reports or logs to assess maturity levels.
Output:
The log file output.log records the code flow and captures required information and errors.

Report:
The Summary sheet in "MaturityScript_automation_templatexlsx" contains resultant values visualized in charts and this can then be used as a data source in PowerBI to get the desired visualization/report.

## API Token Generation
Follow the steps as mentioned in the link below to create/generate tokens:
https://docs.dynatrace.com/docs/shortlink/api-authentication#create-token

## Issues & Troubleshooting
Common issues – API failure.

Common error messages and meanings – TRUE, FALSE, API Failed, Not Available.

Debugging Tips
Tips for troubleshooting and debugging – Validate API connectivity and generated logs post script execution to determine the execution failure results.

## Best Practices
Token Management
Best practices for secure token management – Ensure the Token is properly managed by the account owners and not generated without proper approvals.

Periodic Execution
Recommendations for running the script periodically every 3 months on accounts to validate the assessment. Check for any project updates before the executions.

Result Interpretation
Use the Power BI template to share the visualized report with the customer. Change the data sources of the Power BI template with the updated Excel report generated with the script execution.

