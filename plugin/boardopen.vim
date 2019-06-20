
function! <SID>JiraVimBoardOpen(name)
    let l:name = JiraVimTrimHelper(a:name)
    echo "Loading board " . l:name
    call check#CheckStorageSession()  

    execute "python3 sys.argv = [\"" . l:name . "\"]"
    execute "python3 python.boards.open.JiraVimBoardOpen(sessionStorage)"
endfunction

function! <SID>JiraVimBoardOpenNoSp(name)
    let l:name = JiraVimTrimHelper(a:name)
    echo "Loading board " . l:name
    call check#CheckStorageSession()

    execute "python3 sys.argv = [\"" . l:name . "\"]"
    execute "python3 python.boards.open.JiraVimBoardOpen(sessionStorage, False)"
endfunction

command! -nargs=1 JiraVimBoardOpen call <SID>JiraVimBoardOpen(<q-args>)
command! -nargs=1 JiraVimBoardOpenNosp call <SID>JiraVimBoardOpenNoSp(<q-args>)
