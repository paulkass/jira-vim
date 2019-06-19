
function! <SID>JiraVimSelectSprint()
    let l:sprintName = JiraVimTrimHelper(getline(line(".")))
    execute "JiraVimSprintOpen " l:sprintName
endfunction

command JiraVimSelectSprint call <SID>JiraVimSelectSprint()
