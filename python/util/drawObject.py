import vim
from ..common.kanbanBoard import KanbanBoard
from ..common.scrumBoard import ScrumBoard
from ..common.sprint import Sprint

ISSUE_FORMATTER = lambda startLine, endLine, maxKeyLen, maxSumLen, textWidth: vim.command("%d,%dTabularize /\\u\+-\d\+\s/r0l%dr0" % (startLine, endLine, textWidth-maxKeyLen-maxSumLen-7))

def drawObject(buf, obj, name, sessionStorage):
    """
    Two important lambda function here are:
        itemExtractor - This function accepts a board and returns a collection of categories with each category containing a name at index 0 and a list of key-value pairs at index 1.

        formatter - This function receives 4 parameters: startLine, endLine, maxKeyLen, and maxSumLen. This is executed after each category is printed, with startLine-endLine being the region where
            the category was printed to, and the maxKeyLen and maxSummLen being the maximum lengths of keys and summaries.

        TODO: Potentially might make sense to generalize this and have multiple fields be possible instead of just 2.
    """

    TEXT_WIDTH = vim.current.window.width

    if isinstance(obj, KanbanBoard):
        filetype = "jirakanbanboardview"
        itemExtractor = lambda b: b.getIssues()
        formatter = ISSUE_FORMATTER
        postfix = "board"
        sessionStorage.assignBoard(obj, buf)
    elif isinstance(obj, ScrumBoard): 
        filetype = "jirascrumboardview"
        itemExtractor = lambda b: b.getSprints()
        # dud function
        formatter = lambda a,b,c,d,e: a 
        postfix = "board"
        sessionStorage.assignBoard(obj, buf)
    elif isinstance(obj, Sprint):
        filetype = "jirasprintview"
        itemExtractor = lambda b: b.getIssues()
        formatter = ISSUE_FORMATTER
        postfix = "sprint"
    else:
        filetype = "jiraboardview"
        itemExtractor = lambda b: b.getIssues()
        formatter = ISSUE_FORMATTER
        postfix = "board"
        sessionStorage.assignBoard(obj, buf)

    items = itemExtractor(obj)

    buf[0] = name + ( " %s" % postfix)
    buf.append("="*(len(name)+7))
    buf.append("")

    # Print the issues by category
    for cat in items:
        buf.append(cat[0].upper()+":")
        buf.append("-"*(len(cat[0])+1))
        startLine = len(buf)+1
        i = cat[1]
        endLine = startLine + len(i)-1
        maxKeyLen = 0
        maxSummLen = 0
        for key, summ in i:
            if len(key) >= maxKeyLen:
                maxKeyLen = len(key)
            if len(summ) >= maxSummLen:
                maxSummLen = len(summ)
            buf.append(key + " " + summ)
        buf.append("")
        formatter(startLine, endLine, maxKeyLen, maxSummLen, TEXT_WIDTH)


    # This has to be at the very end, since we must write all of our changes and then set the modifiable to off
    vim.command("setl filetype=%s" % filetype)
