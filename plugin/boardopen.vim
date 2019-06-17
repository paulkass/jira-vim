
function! JiraVimBoardOpen(name)
    echo "Loading board " . a:name
    call check#CheckStorageSession()  

    setl modifiable
    execute "python3 sys.argv = [\"" . a:name . "\"]"
    execute "python3 python.boards.open.JiraVimBoardOpen(sessionStorage)"
    setl nomodifiable
endfunction

function! JiraVimBoardOpenNoSp(name)
    echo "Loading board " . a:name
    call check#CheckStorageSession()  

    setl modifiable
    execute "python3 sys.argv = [\"" . a:name . "\"]"
    execute "python3 python.boards.open.JiraVimBoardOpen(sessionStorage, False)"
    setl nomodifiable
endfunction
