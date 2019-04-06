
function! JiraVimBoardOpen(name)
    echom "Loading board " . a:name
    execute "python3 sys.argv = [\"" . a:name . "\"]"
    execute "python3 import python.boards.open"
endfunction
