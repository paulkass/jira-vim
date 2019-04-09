
" Add the python package directory to path
let s:python_dir = expand("<sfile>:p:h") . "/"
execute "python3 import sys"
execute "python3 sys.path.append('" . s:python_dir . "../')"
execute "python3 import python.boards.open"
execute "python3 import python.issues.open"

let s:addRuntimePath = expand("<sfile>:p:h")."/../after/"
let &runtimepath.=",".s:addRuntimePath
