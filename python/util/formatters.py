
import functools
import vim

class Formatters:
    """
    A class for various formatter functions. A formatter function is usually
    passed into the DrawUtil.draw_category method. Each formatter must accept
    exactly five postiional arguments:
        startLine,
        endLine,
        maxKeyLen,
        maxSumLen,
        textWidth
    You can use keyword arguments to pass in values with FormatterFactory
    below. More information about formatter functions can be found in the
    documentation for DrawUtil.draw_category method.
    """
    @staticmethod
    def ISSUE_FORMATTER(startLine, endLine, maxKeyLen, maxSumLen, textWidth):
        """
        This is the formatter for an issue line. The format of the issues is so
        that the key is on the left side of the line and the summary is as far
        to the right side as possible. This is done by computing the maximum
        space between any two issue keys and summaries and inserting it in
        between the keys and summaries as a "tab". This is the reason why the
        min_space_between variable exists.
        """

        # -7 offset is screen specific, seems it's necessary for normal displays (??)
        min_space_between = textWidth-maxKeyLen-maxSumLen-7
        vim.command("%d,%dTabularize /\\u\+-\d\+\s/r0l%dr0" % (startLine, endLine, min_space_between))
        return endLine

    @staticmethod
    def DISPLAY_FIELDS_FORMATTER(startLine, endLine, *args):
        """
        This is the formatter for the Display Fields of an Issue object. This
        method takes the startLine, and formats everything until the endLine,
        inclusive, with `gqq`.
        """
        vim.command("normal! %dG" % startLine)
        vim.command("normal! %dgqq" % (endLine - startLine + 1))
        return vim.current.window.cursor[0]


    @staticmethod
    def COMMENT_FORMATTER(startLine, endLine, *args, number_of_comments=1):
        """
        This is the formatter for the Comment section of an issue view. It
        formats each single comment one at a time with `gq`, which is why the
        number of comments is needed to perform this operation. It uses
        mappings defined in `ftplugin/jiraissueview.vim` to select the comment
        and navigate between them.
        """
        vim.command("normal! %dG" % startLine)
        for _ in range(number_of_comments):
            vim.command("silent exe \"normal gqncc\"")
            vim.command("silent exe \'/\' . b:commentPattern")
        return vim.current.window.cursor[0]

class FormatterFactory:
    """
    This is factory for creating formatters that rely on more parameters than
    passed in, that is that depend on more values than the five that define a
    formatter function. This classes uses the partial to return a formatter
    with all of the keyword arguments pre-filled, so that you can pass the
    function to the draw_category method.
    """
    @staticmethod
    def get_comment_formatter(number_of_comments):
        return functools.partial(Formatters.COMMENT_FORMATTER, number_of_comments=number_of_comments)
