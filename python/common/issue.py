
class Issue:
    def __init__(self, issueKey, connection):
        self.connection = connection
        jira = self.connection.getJiraObject()

        self.issueKey = issueKey
        self.obj = jira.issue(issueKey)
        self.fields = self.obj.fields
        self.issueId = self.obj.id

        self.displayFields = ["summary", "description"]

    def getField(self, field):
        """
        Returns the value of the field.

        Returns the value of the field belonging to this particular issue.

        Parameters
        ----------
        field : String
            A string that specifies the desired field

        Returns
        -------
        Object (usually String)
            String that represents value of the field of this particular issue.

        """
        return self.fields.__dict__.get(field)

