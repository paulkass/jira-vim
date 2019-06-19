
function! <SID>JiraVimReturn()
    set modifiable
    if exists("b:boardBufferNumber") && b:boardBufferNumber !=? ""
        execute "buffer " . b:boardBufferNumber
    else
        throw "Could not identify the return board buffer. Are you sure you are supposed to be calling this?"
    endif
endfunction

command! JiraVimReturn call <SID>JiraVimReturn()

