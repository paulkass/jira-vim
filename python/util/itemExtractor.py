
class CustomRequestItemExtractor:
    """
    This class is designed to be an iterator that iterates over some items presented by Jira.
    """

    def __init__(self, connection, connection_string, provider, batch_size=10, key="issues"):
        """
        Initializes an iterator for retrieving a Jira resource with pagination.

        This initializes an iterator that provides resources in batches based on the resource defined by the connection string and values provided in the provider function.

        Parameters
        ----------
        connection : Connection
            Connection object to be used to retrieve the resources from Jira.
        connection_string : String
            This is the string that is passed as a custom Request to retrieve resources. Values that depend on the object must be formatted in and passed in with the provider function.
        provider : Lambda
            This is a lambda that takes in no arguments and returns a tuple (with any number of values) that contain the arguments to be formatted into the connection_string.
        key : String (Optional)
            This argument references the results key. This is helpful to count how many items have been extracted, and determine if we've consumed all of them. Defaults to "issues".
        batch_size : Integer (Optional)
            This is an optional argument that sets the batch size for retrieval.

        Returns
        -------
        Nothing

        """

        self.start_at_marker = 0
        self.connection_string = connection_string
        self.connection = connection
        self.provider = provider
        self.batch_size = batch_size
        self.key = key
        self.finished = False

    def __iter__(self):
        return self

    def __next__(self):
        """
        Returns the next batch of resources from Jira.

        Takes the start position, and returns the next <batch_size> resources from Jira through the connection. If no more exist, will continue to increment self.start_at_marker, so it's not safe to call continuously until new resources appear in Jira.

        Parameters
        ----------
        None

        Returns
        -------
        String
            JSON String returned by the connection

        """

        request_string = (self.connection_string + "&startAt=%d&maxResults=%d") % (self.provider() + (self.start_at_marker, self.batch_size))
        resources_response = self.connection.customRequest(request_string).json()
        self.start_at_marker = resources_response["startAt"]
        results_count = 0 if self.key not in resources_response else len(resources_response[self.key])
        self.start_at_marker += results_count
        if results_count < self.batch_size:
            self.finished = True
        return resources_response

    def reset(self):
        """
        Reset the extractor.

        Resets the extractor to allow the for another round of item retrieval.

        Parameters
        ----------
        None

        Returns
        -------
        Nothing

        """

        self.start_at_marker = 0
        self.finished = False

    @staticmethod
    def create_column_issue_extractor(board, column, batch_size=10):
        """
        Create a CustomRequestItemExtractor that extracts only items from one column.

        Create a CustomRequestItemExtractor that creates an extractor only for statuses associated with a specific column of a board.

        Parameters
        ----------
        board : Board
            The board object from which we are extracting the issues
        column : String
            The column name of the column to be extracted
        batch_size : Integer (Optional)
            Optional batch size

        Returns
        -------
        CustomRequestItemExtractor
            CustomRequestItemExtractor instance that gets issues from this particular column

        """

        return CustomRequestItemExtractor(board.connection, board.baseUrl+"/issue?fields=%s&jql=status IN (%s)", lambda: (','.join(board.requiredProperties), ','.join(['\'%s\'' % k for k, v in board.statusToColumn.items() if v == column])), batch_size)


class ObjectItemExtractor:
    """
    This class is designed to be an iterator over issues presented by methods of the JIRA object
    """

    def __init__(self, connection, provider, cleaner, batch_size=10):
        """
        Initializes an item extractor from a function.

        Unlike its counterpart above, this class is better suited to extract results from a JIRA object function. You specify the function, and then this will return an extractor of issues with that given function.

        Parameters
        ----------
        provider : Lambda
            The provider function is a function that takes two keyword arguments: startAt, and maxResults, and returns some result. This result is then piped to the cleaner.
        cleaner : Lambda
            The cleaner lambda is a function that accepts whatever is returned by the cleaner, and returns two things:
                1. the new startAt
                2. Number of items returned
                3. the cleaned result of the item extraction.
            The new startAt is saved, and the results are returned to the user.
        batch_size : Integer (Optional)
            This is an integer that specifies the batch_size, used mostly to specify the "maxResults" parameter of the provider function. Defaults to 10.

        Returns
        -------
        Nothing

        """

        self.start_at_marker = 0
        self.provider = provider
        self.cleaner = cleaner
        self.batch_size = 10
        self.finished = False

    def __iter__(self):
        return self

    def __next__(self):
        if self.finished:
            return []

    def reset(self):
        self.start_at_marker = 0
        self.finished = False
