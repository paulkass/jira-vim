
import sys
from datetime import datetime
import vim
from ..common.issue import Issue
from ..util.drawUtil import DrawUtil

# Arguments are expected through sys.argv
def JiraVimIssueOpen(sessionStorage, isSplit=False):
    issueKey = str(sys.argv[0])
    connection = sessionStorage.connection
    filetype = "jiraissueview"
    # Carry on the board name from the previous buffer

    buf, new = sessionStorage.getBuff(objName=issueKey)
    if isSplit:
        vim.command("sbuffer "+str(buf.number))
    else:
        vim.command("buffer "+str(buf.number))
    vim.command("set modifiable")
    vim.command("setl filetype=%s" % filetype)
    if new:
        issue = Issue(issueKey, connection)
        project = str(issue.getField("project"))
        issue_type = str(issue.getField("issuetype"))

        sessionStorage.assignIssue(issue, buf)

        line = DrawUtil.draw_header(buf, issue, "%s %s" % (issueKey, project)) + 2
        buf.append(issue_type, 2)

        basic_info_category = ("Basic Information", [(field.title(), issue.getField(field)) for field in issue.basicInfo])
        line = DrawUtil.draw_category(buf, issue, basic_info_category, line=line, str_generator=': '.join) + 1
        buf.append("")

        def formatter(startLine, endLine, *args):
            vim.command("normal! %dG" % startLine)
            vim.command("normal! %dgqq" % (endLine - startLine + 1))
            return vim.current.window.cursor[0]

        categories = [(field.title(), [("", issue.getField(field))]) for field in issue.displayFields]
        for c in categories:
            line = DrawUtil.draw_category(buf, issue, c, line=line, formatter=formatter, str_generator=''.join) + 1
            buf.append("")

        comments = issue.getComments()
        # This is just a very long way of formatting each comment as <author> <date>: <body>
        comments = ("Comments", [(str(c.author) + "[" + str(c.author.name) + "] " + datetime.strptime(c.created, "%Y-%m-%dT%H:%M:%S.%f%z").strftime("%c"), c.body) for c in comments])

        def comment_formatter(startLine, endLine, *args):
            vim.command("normal! %dG" % startLine)
            for _ in range(len(comments[1])):
                vim.command("silent exe \"normal gqncc\"")
                vim.command("silent exe \'/\' . b:commentPattern")
            return vim.current.window.cursor[0]

        line = DrawUtil.draw_category(buf, issue, comments, line=line, formatter=comment_formatter, str_generator=": ".join)

    vim.command("set nomodifiable")
    vim.command("normal! gg")
