
function! JiraVimSprintOpen(name)
    echo "Loading sprint " . a:name
    call check#CheckStorageSession()

    setl modifiable
    execute "python3 sys.argv = [\"" . a:name . "\"]"
    execute "python3 python.sprints.open.JiraVimSprintOpen(sessionStorage, False)" 
    setl nomodifiable
endfunction
