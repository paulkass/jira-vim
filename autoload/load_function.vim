
function! load_function#LoadSessionStorage()
    " Add the python package directory to path
    python3 from python.common.sessionObject import SessionObject

" Weird indent so Python indents don't act weird
python3 << EOF
sessionStorage = SessionObject()
EOF

    " Import all scripts with functions here
    python3 import python.boards.open
    python3 import python.issues.open
endfunction
