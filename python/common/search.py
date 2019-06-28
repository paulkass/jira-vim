
class Search:
    def __init__(self, query, connection):
        self.connection = connection
        jira = self.connection.getJiraObject()
         
