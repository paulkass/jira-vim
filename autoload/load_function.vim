
function! load_function#LoadSessionStorage()
    " Add the python package directory to path
    python3 from python.common.sessionObject import SessionObject

" Weird indent so Python indents don't act weird
python3 << EOF
sessionStorage = SessionObject()
EOF

endfunction
