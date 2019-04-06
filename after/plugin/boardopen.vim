
function! JiraVimBoardOpen(name)
    execute "python3 sys.argv = [\"" . a:name . "\"]"
    execute "python3 print(sys.path)"
    execute "python3 import python.boards.open"
endfunction
