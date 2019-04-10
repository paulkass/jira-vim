
" Add the python package directory to path
let s:python_dir = expand("<sfile>:p:h") . "/"
execute "python3 import sys"
execute "python3 sys.path.append('" . s:python_dir . "../')"
python3 from python.common.sessionObject import SessionObject

python3 << EOF
sessionStorage = SessionObject()
EOF

" Import all scripts with functions here
python3 import python.boards.open
python3 import python.issues.open

" Expand runtime path to the after/plugin/ directory
let s:addRuntimePath = expand("<sfile>:p:h")."/../after/"
let &runtimepath.=",".s:addRuntimePath
