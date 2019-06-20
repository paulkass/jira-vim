
function! <SID>JiraVimIssueOpen(name)
    let l:name = JiraVimTrimHelper(a:name)
    echom "Loading issue " . l:name
    call check#CheckStorageSession()  

    execute "python3 sys.argv = [\"" . l:name . "\"]"
    execute "python3 python.issues.open.JiraVimIssueOpen(sessionStorage)"
endfunction

function! <SID>JiraVimIssueOpenSp(name)
    let l:name = JiraVimTrimHelper(a:name)
    echom "Loading issue " . l:name
    call check#CheckStorageSession()  

    execute "python3 sys.argv = [\"" . l:name . "\"]"
    execute "python3 python.issues.open.JiraVimIssueOpen(sessionStorage, True)"
endfunction

command -nargs=1 JiraVimIssueOpen call <SID>JiraVimIssueOpen(<q-args>)
command -nargs=1 JiraVimIssueOpenSp call <SID>JiraVimIssueOpenSp(<q-args>)
