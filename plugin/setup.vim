
let s:script_dir = expand("<sfile>:p:h") . "/"

" Make sure that all the necessary parts are in place {{{
if !has('python3')
    throw "No python3 function found. Read the jiravim-python3-compile help section for more information."
endif

execute "python3 import sys"
execute "python3 sys.path.append('" . s:script_dir . "../')"

" Check that all pip dependencies are installed
python3 import python.util.pip_check
let s:status = py3eval("python.util.pip_check.check()")
if s:status == 1
    " throw "Please consult the 'jiravim-pip-install' help tag for help on installing pip dependencies."
    finish
endif

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


" }}}

" Globally used python and vim functions/scripts {{{

" Import all scripts with functions here
python3 import jira
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
