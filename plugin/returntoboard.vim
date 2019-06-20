
function! <SID>JiraVimReturn()
    """
    " This Function is designed to switch to the window with the board buffer
    " loaded. If no window like that exists, it loads the buffer in the
    " current window.
    """
    set modifiable
    if exists("b:boardBufferNumber") && b:boardBufferNumber !=? ""
        let l:bufferWindow = bufwinnr(b:boardBufferNumber)
        if l:bufferWindow !=? -1
            execute l:bufferWindow "wincmd w" 
        else
            execute "buffer " . b:boardBufferNumber
        endif
    else
        throw "Could not identify the return board buffer. Are you sure you are supposed to be calling this?"
    endif
endfunction

command! JiraVimReturn call <SID>JiraVimReturn()

