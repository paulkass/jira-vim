function! <SID>JiraVimSelectIssue(command)
    let l:command = JiraVimTrimHelper(a:command)
    call check#CheckStorageSession()
    if -1 !=# matchstr(&filetype, g:jiraBoardFiletypePattern)  
        let l:bufferNumber = bufnr("%") 
        let l:line = getline(line("."))
        let l:issueMatch = JiraVimTrimHelper(matchstr(l:line, '\v\u+-\d+\s'))
        if l:issueMatch != ""
            execute l:command " " l:issueMatch
            let b:boardBufferNumber = l:bufferNumber 
        endif
    else
        throw "The current buffer is not a board, are you sure you should be calling this command?"
    endif
endfunction

command -nargs=1 -complete=command JiraVimSelectIssue call <SID>JiraVimSelectIssue(<q-args>)

" Convenience commands for split and nosplit
command JiraVimSelectIssueNosp call <SID>JiraVimSelectIssue("JiraVimIssueOpen")
command JiraVimSelectIssueSp call <SID>JiraVimSelectIssue("JiraVimIssueOpenSp")
