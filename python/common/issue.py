
class Issue:
    def __init__(self, issueKey, connection):
        self.connection = connection
        jira = self.connection.getJiraObject()

        self.issueKey = issueKey
        self.obj = jira.issue(issueKey)
        self.fields = self.obj.fields
        self.issueId = self.obj.id

        # These fields will be displayed in normal category style on issue views
        self.displayFields = ["summary", "description"]

        # These fields will be displayed in the Basic Information section
        self.basicInfo = ["status", "reporter", "assignee"]
        print(self.obj.fields.__dict__)

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
        return str(self.fields.__dict__.get(field))

