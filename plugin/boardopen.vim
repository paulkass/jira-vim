
let s:python_dir = expand("<sfile>:p:h") . "/"

function! JiraVimBoardOpen(name)
    vnew
    set filetype=jiraboardview
    silent "python3 sys.argv = [\"" . a:name . "\"]"
    " For debugging, switch from execute to silent
    execute "py3file " . s:python_dir . "../python/boards/open.py"
endfunction
