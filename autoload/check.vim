

function! check#CheckStorageSession()
    " Invert the values of 0 and 1 since we want to only do something if the
    " object does not exist
    let b = py3eval("0 if 'sessionStorage' in {**globals(), **locals()} else 1")
    if b
       call load_function#LoadSessionStorage()
    endif
endfunction
