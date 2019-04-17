
let s:python_dir = expand("<sfile>:p:h") . "/"
execute "python3 import sys"
execute "python3 sys.path.append('" . s:python_dir . "../')"
