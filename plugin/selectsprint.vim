
function! JiraVimSelectSprint()
    let l:line = getline(line("."))
    let l:sprintName = substitute(l:line, '\v\s+$', '', 'g')
    call JiraVimSprintOpen(l:sprintName)
endfunction
