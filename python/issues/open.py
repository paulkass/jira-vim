
import sys
from datetime import datetime
import vim

from ..util.formatters import Formatters, FormatterFactory
from ..common.issue import Issue
from ..util.drawUtil import DrawUtil

# Arguments are expected through sys.argv
def JiraVimIssueOpen(sessionStorage, isSplit=False):
    issueKey = str(sys.argv[0])
    connection = sessionStorage.connection
    # Carry on the board name from the previous buffer

    buf, new = sessionStorage.getBuff(objName=issueKey)
    if isSplit:
        vim.command("sbuffer "+str(buf.number))
    else:
        vim.command("buffer "+str(buf.number))
    vim.command("set modifiable")
    if new:
        issue = Issue(issueKey, connection)
        project = str(issue.getField("project"))
        issue_type = str(issue.getField("issuetype"))
        DrawUtil.set_filetype(issue)

        sessionStorage.assignIssue(issue, buf)

        ##### DRAW THE HEADER
        line = DrawUtil.draw_header(buf, issue, "%s %s" % (issueKey, project)) + 2
        buf.append(issue_type, 2)

        ##### DRAW BASIC INFORMATION
        basic_info_category = ("Basic Information", [(field.title(), issue.getField(field)) for field in issue.basicInfo])
        line = DrawUtil.draw_category(buf, issue, basic_info_category, line=line, str_generator=': '.join) + 1
        buf.append("")

        ##### DRAW DISPLAY FIELDS
        categories = [(field.title(), [("", issue.getField(field))]) for field in issue.displayFields]
        for c in categories:
            line = DrawUtil.draw_category(buf, issue, c, line=line, formatter=Formatters.DISPLAY_FIELDS_FORMATTER, str_generator=''.join) + 1
            buf.append("")

        ##### DRAW COMMENTS
        comments = issue.getComments()
        comments = ("Comments", [(str(c.author) + "[" + (str(c.author.name) if hasattr(c.author, "name") else str(c.author.accountId)) + "] " + datetime.strptime(c.created, "%Y-%m-%dT%H:%M:%S.%f%z").strftime("%c"), c.body) for c in comments])
        # This is just a very long way of telling the computer to format each comment as <author> <date>: <body>
        # The %c in strftime is to format the date in a human readable way
        comment_formatter = FormatterFactory.get_comment_formatter(len(comments[1]))
        line = DrawUtil.draw_category(buf, issue, comments, line=line, formatter=comment_formatter, str_generator=": ".join) + 1
        buf.append("")

    vim.command("set nomodifiable")
    vim.command("normal! gg")
