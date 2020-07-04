

function! check#CheckStorageSession()

    " Check that credential variables are set
    if !exists("g:jiraVimDomainName")
        throw "Please set 'g:jiraVimDomainName'. Refer to the 'jiravim-credentials' help tag for more information."
    endif

    if !exists("g:jiraVimEmail")
        throw "Please set 'g:jiraVimEmail'. Refer to the 'jiravim-credentials' help tag for more information."
    endif

    if !exists("g:jiraVimToken")
        throw "Please set 'g:jiraVimToken'. Refer to the 'jiravim-credentials' help tag for more information."
    endif

    " Invert the values of 0 and 1 since we want to only do something if the
    " object does not exist
    let l:storage_exists = py3eval("0 if 'sessionStorage' in {**globals(), **locals()} else 1")
    if l:storage_exists
        call load_function#LoadSessionStorage()
    endif
endfunction
