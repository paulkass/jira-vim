
function! JiraVimIssueOpen(name)
    echom "Loading issue " . a:name
    call check#CheckStorageSession()  

    set modifiable
    execute "python3 sys.argv = [\"" . a:name . "\"]"
    execute "python3 python.issues.open.JiraVimIssueOpen(sessionStorage)"
    set nomodifiable
endfunction

function! JiraVimIssueOpenSp(name)
    echom "Loading issue " . a:name
    call check#CheckStorageSession()  

    set modifiable
    execute "python3 sys.argv = [\"" . a:name . "\"]"
    execute "python3 python.issues.open.JiraVimIssueOpen(sessionStorage, True)"
    set nomodifiable
endfunction
