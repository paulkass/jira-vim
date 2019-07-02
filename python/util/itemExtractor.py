
class ObjectItemExtractor:
    """
    This class is designed to be an iterator over issues presented by methods of the JIRA object
    """

    def __init__(self, provider, batch_size=10):
        """
        Initializes an item extractor from a function.

        Unlike its counterpart above, this class is better suited to extract results from a JIRA object function. You specify the function, and then this will return an extractor of issues with that given function.

        Parameters
        ----------
        provider : Lambda
            The provider function is a function that takes two keyword arguments: startAt and maxResults. The result is a list of items (it must be an object such that passing it to the len() function should return the number of items).
        batch_size : Integer (Optional)
            This is an integer that specifies the batch_size, used mostly to specify the "maxResults" parameter of the provider function. Defaults to 10.

        Returns
        -------
        Nothing

        """

        self.start_at_marker = 0
        self.provider = provider
        self.batch_size = 10
        self.finished = False

    def __iter__(self):
        return self

    def __next__(self):
        if self.finished:
            return []
        results = self.provider(self.start_at_marker, self.batch_size)
        num_items = len(results)
        if num_items < self.batch_size:
            self.finished = True
        self.start_at_marker += num_items
        return results

    def reset(self):
        self.start_at_marker = 0
        self.finished = False

    @staticmethod
    def create_column_issue_extractor(board, column, batch_size=10):
        """
        Creates a simple extractor for issues from a certain column

        Creates an extractor for issues in a column. This is to replace the previously used CustomRequestItemExtractor class.

        Parameters
        ----------
        board : Board
            Board from which the issues will be extracted.
        column : String
            Name of the column to be matched
        batch_size : Integer (Optional)
            Batch size. Defaults to 10.

        Returns
        -------
        ObjectItemExtractor
        """
        def provider(startAt, maxResults=batch_size):
            connection_string = board.baseUrl+"/issue?fields=%s&jql=status IN (%s)"
            req_fields_list = ','.join(board.requiredProperties)
            req_status_list = ','.join(['\'%s\'' % k for k, v in board.statusToColumn.items() if v == column])
            req_vars = (req_fields_list, req_status_list) + (startAt, maxResults)
            request_string = (connection_string + "&startAt=%d&maxResults=%d") % (req_vars)

            response = board.connection.customRequest(request_string).json()
            return response["issues"]
        return ObjectItemExtractor(provider, batch_size=batch_size)

    @staticmethod
    def create_search_extractor(connection, query, batch_size=10):
        """
        Create a simple extractor for a search query.

        This creates an ObjectItemExtractor from a connection and a search query. It usses the search_issues method of the JIRA object.

        Parameters
        ----------
        connection : Connection
            A connection object from which the JIRA object is extracted.
        query : String
            A search query. This is inputted into the search_issues method of the JIRA object.
        batch_size : Integer (Optional)
            Batch size for the issue extraction. Defaults to 10.

        Returns
        -------
        ObjectItemExtractor
        """
        provider = lambda startAt, maxResults: connection.getJiraObject().search_issues(query, startAt=startAt, maxResults=maxResults)
        return ObjectItemExtractor(provider, batch_size)

