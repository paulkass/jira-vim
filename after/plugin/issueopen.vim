
function! JiraVimIssueOpen(name)
    echom "Loading issue " . a:name
    execute "python3 sys.argv = [\"" . a:name . "\"]"
    execute "python3 python.issues.open.JiraVimIssueOpen()"
endfunction
