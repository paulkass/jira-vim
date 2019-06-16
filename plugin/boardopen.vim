
function! JiraVimBoardOpen(name)
    echo "Loading board " . a:name
    call check#CheckStorageSession()  

    set modifiable
    execute "python3 sys.argv = [\"" . a:name . "\"]"
    execute "python3 python.boards.open.JiraVimBoardOpen(sessionStorage)"
    set nomodifiable
endfunction

function! JiraVimBoardOpenNoSp(name)
    echo "Loading board " . a:name
    call check#CheckStorageSession()  

    set modifiable
    execute "python3 sys.argv = [\"" . a:name . "\"]"
    execute "python3 python.boards.open.JiraVimBoardOpen(sessionStorage, False)"
    set nomodifiable
endfunction
