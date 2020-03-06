
from jira.resources import Issue as JiraIssue

class Issue:
    def __init__(self, issueKey, connection):
        self.connection = connection
        jira = self.connection.getJiraObject()

        if isinstance(issueKey, JiraIssue):
            self.obj = issueKey
            self.issueKey = self.obj.key
        else:
            self.obj = jira.issue(issueKey)
            self.issueKey = issueKey
        self.fields = self.obj.fields
        self.issueId = self.obj.id

        # These fields will be displayed in normal category style on issue views
        self.displayFields = ["summary", "description"]

        # These fields will be displayed in the Basic Information section
        self.basicInfo = ["status", "reporter", "assignee"]

    def getField(self, field, as_str=True):
        """
        Returns the value of the field.

        Returns the value of the field belonging to this particular issue.

        Parameters
        ----------
        field : String
            A string that specifies the desired field
        as_str : Boolean (Optional)
            Specifies whether to return the property in string format. Defaults to True

        Returns
        -------
        Object (usually String)
            String that represents value of the field of this particular issue.

        """
        obj = self.fields.__dict__.get(field)
        return str(obj) if as_str else obj

    def getComments(self):
        """
        Returns a list of columns.

        Returns a list of column objects that contain information about the columns.

        Parameters
        ----------
        None

        Returns
        -------
        Nothing

        """

        comment_obj = self.getField("comment", as_str=False)
        return comment_obj.comments

