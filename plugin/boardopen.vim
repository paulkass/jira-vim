
let s:python_dir = expand("<sfile>:p:h") . "/"

function! JiraVimBoardOpen(name)
    execute "python3 import sys"
    execute "python3 sys.argv = [\"" . a:name . "\"]"
    " For debugging, switch from execute to silent
    execute "py3file " . s:python_dir . "../python/common/board.py"
    execute "py3file " . s:python_dir . "../python/common/connection.py"
    execute "py3file " . s:python_dir . "../python/boards/open.py"
endfunction
