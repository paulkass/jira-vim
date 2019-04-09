import json
from jira import JIRA

class Issue:
    def __init__(self, issueKey, connection):
        self.issueKey = issueKey
        self.connection = connection
        jira = self.connection.getJiraObject()
        self.obj = jira.issue(issueKey)
        self.id = self.obj.id
