
let s:python_dir = expand("<sfile>:p:h") . "/"
execute "python3 import sys"
execute "python3 sys.path.append('" . s:python_dir . "../')"
" Expand runtime path to the after/plugin/ directory
let s:addRuntimePath = expand("<sfile>:p:h")."/../after/"
let &runtimepath.=",".s:addRuntimePath
