
class ItemCategorizer():

    @staticmethod
    def issueCategorizer(issues, statusToColumn):
        """
        Categorizes issues based on category.

        Categorizes issues based on the status to column mappings. NOTE: THIS DOES NOT CREATE ISSUE OBJECTS

        Parameters
        ----------
        issues : String
            A json string containing an "issues" field that contains an array of issues to be processed.
        statusToColumn : Dict
            A dictionary that maps status to columns. This is a many to one relationship.

        Returns
        -------
        List
            a list that contains tuples of (column, <list of issue keys>) for each column in the columnToIssues dict.

        """

        columnToIssues = {}
        for i in issues:
            key = (i["key"], i["fields"]["summary"])
            statusId = i["fields"]["status"]["id"]
            column = statusToColumn[statusId]
            if column not in columnToIssues:
                columnToIssues[column] = set()
            columnToIssues[column].add(key)
        return [(a, list(b)) for a, b in columnToIssues.items() if len(b) > 0]
