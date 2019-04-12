
function! JiraVimIssueOpen(name)
    echom "Loading issue " . a:name
    execute "python3 sys.argv = [\"" . a:name . "\"]"
    execute "python3 python.issues.open.JiraVimIssueOpen(sessionStorage)"
endfunction

function! JiraVimIssueOpenSp(name)
    echom "Loading issue " . a:name
    execute "python3 sys.argv = [\"" . a:name . "\"]"
    execute "python3 python.issues.open.JiraVimIssueOpen(sessionStorage, True)"
endfunction
