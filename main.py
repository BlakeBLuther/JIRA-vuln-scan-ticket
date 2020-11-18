#!/usr/bin/env python

import os
import jira
from google.cloud import secretmanager

JIRA_URL = 'https://uplightinc.atlassian.net'
CHRIS_ACCOUNT_ID = '5f7b9de06029960076d87bee'
BLAKE_ACCOUNT_ID = '5fa17d950eb8b4006965ae49'
USERNAME = 'blake.luther@uplight.com'
TASK_DESC = '''Vulnerability Scan Review Procedure

Resolve this ticket by executing the following steps:

    # Retrieve the latest vulnerability scan report from ThreatStack
    # Inspect report for any High Criticality vulnerabilities
    # Create sub-tasks and plan for patching any High findings with CESA notices
    # Document action items for other non-CESA notice findings

'''

client = secretmanager.SecretManagerServiceClient()
secret_name = "JIRA-api-key-blake"
project_id = "security-automation-295920"
request = {"name": f"projects/{project_id}/secrets/{secret_name}/versions/latest"}
response = client.access_secret_version(request)
api_key = response.payload.data.decode("UTF-8").strip()
# api_key is now the JIRA key, pulled from GCP


def JIRA_vuln_scan_ticket(inc_request):
    jcon = jira.JIRA(JIRA_URL, basic_auth=(USERNAME,api_key))
    issue = {
        'project': 'SEC',
        'summary': 'Weekly network vulnerability scan handling',
        'description': TASK_DESC,
        'issuetype': {'name': 'Task'},
        'assignee': {'accountId': CHRIS_ACCOUNT_ID}
    }
    new_issue = jcon.create_issue(fields=issue)
    return "Done :)"