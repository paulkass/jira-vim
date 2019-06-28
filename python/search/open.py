
import vim

def JiraVimSearchOpen(sessionStorage):
    searchargs = str(sys.argv[0])
    connection = sessionStorage.connection
    filetype = "jirasearchview"

    buf, new = sessionStorage.getBuff(objId="")
