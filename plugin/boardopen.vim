
function! JiraVimBoardOpen(name)
    echo "Loading board " . a:name
    call check#CheckStorageSession()  
    execute "python3 sys.argv = [\"" . a:name . "\"]"
    execute "python3 python.boards.open.JiraVimBoardOpen(sessionStorage)"
endfunction

function! JiraVimBoardOpenNoSp(name)
    echo "Loading board " . a:name
    call check#CheckStorageSession()  
    execute "python3 sys.argv = [\"" . a:name . "\"]"
    execute "python3 python.boards.open.JiraVimBoardOpen(sessionStorage, False)"
endfunction
