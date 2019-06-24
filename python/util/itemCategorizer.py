
class ItemCategorizer():

    @staticmethod
    def issueCategorizer(issues, statusToColumn, columnExtractors):
        """
        Categorizes issues based on category.

        Categorizes issues based on the status to column mappings. NOTE: THIS DOES NOT CREATE ISSUE OBJECTS

        Parameters
        ----------
        issues : String
            A json string containing an "issues" field that contains an array of issues to be processed.
        statusToColumn : Dict
            A dictionary that maps status to columns. This is a many to one relationship.
        columnExtractos : Dict
            A dictionary that maps columns to the extractor. Used only to assign the "more" parameter, that is to see if the extractor is finished.

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
                columnToIssues[column] = list()
            columnToIssues[column].append(key)
        return [(a, not columnExtractors[a].finished, b) for a, b in columnToIssues.items() if len(b) > 0]
