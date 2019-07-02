
let s:script_dir = expand("<sfile>:p:h") . "/"
execute "python3 import sys"
execute "python3 sys.path.append('" . s:script_dir . "../')"

" Make sure that all the necessary parts are in place {{{
if !has('python3')
    throw "No python3 function found. Read the jiravim-python3-compile help section for more information."
endif

" Check that all pip dependencies are installed
python3 import python.util.pip_check

" Install Tabular submodule
silent let s:gitOutput = system("git")
if !matchstr(s:gitOutput, '\vgit:\ command\ not\ found')
    silent call system("git submodule init " . s:script_dir . "../tabular")
    silent call system("git submodule update " . s:script_dir . "../tabular")
endif

" Check that Tabularize command from Tabular is available
if !exists(":Tabularize")
    " The dot between script_dir and the rest of the path is avoid a space in
    " the path definition
    execute "source" s:script_dir . "../tabular/plugin/Tabular.vim"
    execute "source" s:script_dir . "../tabular/autoload/tabular.vim"
    execute "source" s:script_dir . "../tabular/after/plugin/TabularMaps.vim"

    if !exists(":Tabularize")
        throw "Couldn't install Tabularize for some reason. Please contact the owner of this project for assistance"
    endif
endif

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

" }}}

" Globally used python and vim functions/scripts {{{

" Import all scripts with functions here
python3 import python.boards.open
python3 import python.boards.more
python3 import python.issues.open
python3 import python.search.open
python3 import python.search.more
python3 import python.sprints.open
python3 import python.sprints.more

" Set some global constants
let g:jiraBoardFiletypePattern = '\vjira\a*boardview'

" Some Plug-in specific Helper functions
function! JiraVimTrimHelper(string)
    let l:arg = substitute(a:string, '\v^\s+', "", "")
    let l:arg = substitute(l:arg, '\v\s+$', "", "")
    return l:arg
endfunction

"}}}
