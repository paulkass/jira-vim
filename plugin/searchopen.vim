
function! <SID>JiraVimSearch(query)
    let l:query = JiraVimTrimHelper(a:query)
    echom "Searching the query ..."
    call check#CheckStorageSession()

    execute "python3 sys.argv = [\"" . l:query . "\"]"
    execute "python3 python.search.open.JiraVimSearchOpen(sessionStorage)"
endfunction

command -nargs=1 JiraVimSearchOpen call <SID>JiraVimSearch(<q-args>)
