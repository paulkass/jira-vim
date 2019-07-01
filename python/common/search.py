
from ..util.itemExtractor import ObjectItemExtractor
from ..common.issue import Issue

class Search:
    def __init__(self, query, connection, batch_size=10):
        self.connection = connection
        self.itemExtractor = ObjectItemExtractor.create_search_extractor(self.connection, query, batch_size=batch_size)

    def getIssues(self):
        """
        Get the next batch of issues.

        Returns a batch of issues.

        Parameters
        ----------
        None

        Returns
        -------
        A standard list of issues categorized in one category.
        """
        # This could be made more efficient
        issues = [Issue(i.key, self.connection) for i in self.itemExtractor.__next__()]
        return [("Search results", not self.itemExtractor.finished, [(i.issueKey, i.getField("summary", as_str=True)) for i in issues])]
