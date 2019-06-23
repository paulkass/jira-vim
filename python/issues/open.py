
import sys
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
    if new:
        issue = Issue(issueKey, connection)
        project = str(issue.getField("project"))
        issue_type = str(issue.getField("issuetype"))

        sessionStorage.assignIssue(issue, buf)

        line = DrawUtil.draw_header(buf, issue, "%s %s" % (issueKey, project)) + 2
        buf.append(issue_type, 2)

        basic_info_category = ("Basic Information", [(field.title(), issue.getField(field)) for field in issue.basicInfo])

        line = DrawUtil.draw_category(buf, issue, basic_info_category, line=line, str_generator=lambda i: ': '.join(i)) + 1
        buf.append("")

        categories = [(field.title(), [("", issue.getField(field))]) for field in issue.displayFields]

        def formatter(startLine, endLine, *args):
            vim.command("normal! %dG" % startLine)
            vim.command("normal! %dgqq" % (endLine - startLine + 1))

        for c in categories:
            line = DrawUtil.draw_category(buf, issue, c, line=line, formatter=formatter, str_generator=lambda item: ''.join(item)) + 1
            buf.append("") 
        
        vim.command("setl filetype=%s" % filetype)
    vim.command("set nomodifiable")
