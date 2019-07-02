from collections import OrderedDict
import vim

from .formatters import Formatters
from ..common.kanbanBoard import KanbanBoard
from ..common.scrumBoard import ScrumBoard
from ..common.board import Board
from ..common.sprint import Sprint
from ..common.issue import Issue
from ..common.search import Search


class DrawUtil():

    MAPPINGS = OrderedDict({
        "kanban": KanbanBoard,
        "scrum": ScrumBoard,
        "board": Board,
        "sprint": Sprint,
        "issue": Issue,
        "search": Search
        })
    RESERVED_KEYWORDS = ["default", "obj"]

    @staticmethod
    def __type_selector(**args):
        """
        This is a helper method to return a value based on the type of an object.

        Many cases here will depend on the type of the object that is being drawn onto a buffer. This means that we need to somehow create mappings to assign crucial parameters depending on the type of the object in question. This method uses an OrderedDict to check the type of the object from bottom to top (so if class A inherits from class B, class A will be checked before class B) and return an appropriate value.

        Parameters
        ----------
        **args: dict
            A dictionary object that may contain the following fields:
                kanban,
                scrum,
                board,
                sprint,
                issue,
                default,
                obj

            The obj mapping is required for the operation to work.

        Returns
        -------
        Some value
            This is the value obtained from the key in the **args dict that corresponds to the most granular class of the object passed in. If the object matches none of the types from **args, use value at key "default". If no default, returns None.

        """

        # Check to see that obj exists and throw an error if it doesn't
        obj = args["obj"]

        for k, c in DrawUtil.MAPPINGS.items():
            if k not in DrawUtil.RESERVED_KEYWORDS and k in args and isinstance(obj, c):
                return args[k]

        return args.get("default", None)

    @staticmethod
    def draw_header(buf, obj, name, formatting=None):
        """
        Draw the header for object.

        Parameters
        ----------
        buf : vim.buffer
            Buffer to be drawn onto
        obj : Object
            The object to examine
        name : String
            The name of the object to be written.
        formatting : Lambda (Optional)
            Specifies the formatting of the first title line. If not specified, defaults to a tabular formatting for issues and a dud (no formatting) for the rest. The lambda accepts one argument, the text width for the window.

        Returns
        -------
        int
            This represents the line number of the blank line under the header. Intended to be a constant since it's expected that this is written at the top of the file.

        """

        text_width = vim.current.window.width

        postfix = DrawUtil.__type_selector(
            board="board",
            sprint="sprint",
            default="",
            obj=obj
            )

        if not formatting:
            formatting = DrawUtil.__type_selector(
                default=lambda w: w,
                issue=lambda w: vim.command("1Tabularize /\\u\+-\d\+\s/r0c%dr0" % (text_width-len(name)-7)),
                obj=obj
                )

        header_str = (name + (" %s" % postfix)).strip()
        buf[0] = header_str
        buf.append("="*len(header_str))
        buf.append("")

        formatting(text_width)

        return 3

    @staticmethod
    def draw_item(buf, item, line=None, str_generator=None):
        """
        Draws an item in the buffer.

        Draws an item on the specified line or at the end of the buffer if no line is specified. Does not apply formatting: formatting is applied when drawing a category.

        Parameters
        ----------
        buf : vim.buffer
            Buffer to be drawn onto
        item : tuple
            Tuple that contains the key and summary of the item
        line : int (Optional)
            Line on which to draw the item. If not specified, appends to the end of the buffer
        str_generator : Lambda (Optional)
            This is a lambda that accepts an item and returns a string that is to be printed. The string can contain multiple lines, in which case the text will be printed line by line and then adjusted. If not specified, joins the key and summary in item with spaces.

        Returns
        -------
        tuple
            the next line, the length of the key, and the length of the summary as a tuple

        """

        if not str_generator:
            str_generator = " ".join

        key, summ = item
        text = str_generator(item)
        line = len(buf)+1 if not line else line

        for strip in text.splitlines():
            buf.append(strip, line-1)
            line += 1

        return line, len(key), len(summ)

    @staticmethod
    def draw_category(buf, obj, category, line=None, more=False, formatter=None, with_header=True, str_generator=None):
        """
        Draws a category in the buffer.

        Gets a category and draws it in the buffer at the specified line. Also applies formatting afterwards.

        Parameters
        ----------
        buf : vim.buffer
            Buffer to be drawn onto
        obj : Object
            Object to be examined
        category : tuple
            Tuple that contains the name of the category and a list of issues
        line : int (Optional)
            Line to be drawn onto (0-indexed). If none exist, defaults to appending to the file.
        more : Boolean (Optional)
            Boolean that determines whether a MORE is displayed at the bottom of the items. Defaults to False.
        formatter : Lambda (Optional)
            Lambda that accepts 5 arguments (
                startLine,
                endLine,
                maxKeyLen,
                maxSummLen,
                window_width
                )
            Lambda returns the position of the endLine (since it might be changed through formatting).
            The values of the variables should be self-explanatory. If not defined, it's chosen depending on the type of object, dud function for scrum boards and Formatters.ISSUE_FORMATTER otherwise.
        with_header : Boolean (Optional)
            Boolean that specifies if the header of the category should be displayed. True by default.
        str_generator : Lambda (Optional)
            Lambda that gets passed in as str_generator field to the draw_item call. Default to None, which in draw_item just adds a space between the key and the summ.

        Returns
        -------
        int
            the line number of the blank line under the last item in the category

        """

        window_width = vim.current.window.width

        # No formatting for the scrum board
        formatter = formatter if formatter else DrawUtil.__type_selector(
            obj=obj,
            scrum=lambda a, b, c, d, e: b,
            issue=lambda a, b, c, d, e: b,
            default=Formatters.ISSUE_FORMATTER
            )

        if not line:
            line = len(buf)+1

        if with_header:
            buf.append(category[0].upper()+":", line-1)
            line += 1
            buf.append("-"*(len(category[0])+1), line-1)
            line += 1

        startLine = line
        items = category[1]
        # Using maxSummLen to clarify that we are measuring the maximum length of the summary
        maxKeyLen, maxSummLen = 0, 0
        for item in items:
            line, lenKey, lenSumm = DrawUtil.draw_item(buf, item, line=line, str_generator=str_generator)
            maxKeyLen = max([lenKey, maxKeyLen])
            maxSummLen = max([lenSumm, maxSummLen])
        endLine = line-1

        vim.command("normal! %dG" % endLine)

        endLine = formatter(startLine, endLine, maxKeyLen, maxSummLen, window_width)
        line = endLine+1

        if more:
            line = DrawUtil.draw_more(buf, line)

        return line

    @staticmethod
    def draw_items(buf, obj, sessionStorage, line=None, itemExtractor=None, withCategoryHeaders=True):
        """
        Draw a set of items from an object.

        This method draws items extracted via itemExtractor from object, and draws them to the buffer.

        Parameters
        ----------
        buf : vim.buffer
            Buffer to be drawn onto
        obj : Object
            Object from which items will be extracted
        sessionStorage : SessionStorage
            The sessionStorage object associated with current session.
        line : int (Optional)
            Line on which to start drawing. If not defined, appends to the end of the buffer
        itemExtractor : Lambda (Optional)
            Lambda that accepts an object and returns a list of items separated by category. If not defined, defaults to calling the getIssues method of the object. Returns a list of tuples with 3 elements each: the name of the category, the "more" parameter, and the list of item keys.
        withCategoryHeaders : Boolean (Optional)
            Boolean that determines whether the headers for the categories will be displayed. True by default.

        Returns
        -------
        int
            the line number of the blank line under the last item in the category

        """

        if not line:
            line = len(buf)+1

        if not itemExtractor:
            itemExtractor = DrawUtil.__type_selector(
                obj=obj,
                default=lambda o: o.getIssues(),
                scrum=lambda o: o.getSprints()
                )

        # Associate buffer with object in sessionStorage
        addBoardFunc = sessionStorage.assignBoard
        addSprintFunc = sessionStorage.assignSprint
        dudFunc = lambda a, b: b
        DrawUtil.__type_selector(
            board=addBoardFunc,
            sprint=addSprintFunc,
            default=dudFunc,
            obj=obj
            )(obj, buf)

        extraction = itemExtractor(obj)

        for cat in extraction:
            more = cat[1]
            item_list = (cat[0], cat[2])
            line = DrawUtil.draw_category(buf, obj, item_list, line, more=more, with_header=withCategoryHeaders) + 1
            buf.append("", line-2)
        return line

    @staticmethod
    def draw_more(buf, line=None):
        """
        Draws the "MORE" symbol for columns representing extracts that have not been fully consumed.

        Parameters
        ----------
        buf : Buffer
            Buffer to be drawn to
        line : Integer (Optional)
            Line to be drawn on. Defaults to the end of the buffer.

        Returns
        -------
        Integer
            returns line + 1

        """

        if not line:
            line = len(buf) + 1

        buf.append("---MORE---", line-1)

        return line+1

    @staticmethod
    def set_filetype(obj, filetype=None):
        """
        Sets filetype in current buffer

        Sets filetype in current buffer depending on the type of object. Recommended to execute this function after you\'ve written any changes since this function with set modifiable to off

        Parameters
        ----------
        obj : Object
            Object to be examined
        filetype : String (Optional)
            Sets the current buffer to specified filetype unless it's none, then selection is done based on type of object

        Returns
        -------
        Nothing

        """
        if not filetype:
            filetype = DrawUtil.__type_selector(
                kanban="jirakanbanboardview",
                scrum="jirascrumboardview",
                sprint="jirasprintview",
                board="jiraboardview",
                issue="jiraissueview",
                search="jirasearchview",
                default="",
                obj=obj
                )

        vim.command("setl filetype=%s" % filetype)

