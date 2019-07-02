# jira-vim

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/5d3c5f54a99b44688ea474d3b0a3fba7)](https://app.codacy.com/app/paul.kassianik/jira-vim?utm_source=github.com&utm_medium=referral&utm_content=paulkass/jira-vim&utm_campaign=Badge_Grade_Settings)
[![Build Status](https://travis-ci.org/paulkass/jira-vim.svg?branch=master)](https://travis-ci.org/paulkass/jira-vim)
[![License](https://img.shields.io/github/license/paulkass/jira-vim.svg)](./LICENSE)

Jira-vim is a way to view your JIRA setup without the bloat of the JIRA UI.

Imagine browsing Jira on your computer. All those buttons, animations, and
fancy UI magic that you don't really need are really slowing down your
computer. It's not improving your productivity, on the contrary it makes you
wait and distract yourself while it loads features you'll never need! So I
created this: an attempt at de-bloating Jira by getting rid of the UI and using
the standard Vim environment that we know and love to display data that we
obtain from the API. 

<p align="center">
  <img src="https://cdn.jsdelivr.net/gh/paulkass/jira-vim/jiravim.svg">
</p>


## Current Status: Working on the beta version

Ahoy, I compiled a tentative checklist of the stuff that will need to be done for the beta release. This checklist is a subset of all the stuff that will be done for the beta, so all the stuff here *will* be done, but this isn't necessarily the exhaustive list of all the things that will be included in the beta release. This also only includes new features, but not any tech debt tasks or technical housekeeping. Here it is:

- [x] Search Functionality
- [ ] Differentiate between various Issue types
- [ ] Colored syntax highlights
- [x] View issues assigned to you
- [ ] Update issue fields
- [ ] Creating new issues

If you have anything to suggest, please let me know! 

You can also see what I'm working on right now by looking at [this github project](https://github.com/paulkass/jira-vim/projects/2).

Also, it will take me a long time to go through each of these checkboxes one by one and make them, so if you have a feature that you particularly like, I encourage you to [contribute](#contributing).

## Installation

With Pathogen, use:

    cd ~/.vim/bundle
    git clone https://github.com/paulkass/jira-vim

With Vim-Plug, use:

    Plug 'paulkass/jira-vim'


### Dependencies on Python

Please compile Vim with python3 for this plugin to function properly.

Then install the `requirements.txt` file with pip. Usually the command is 

    pip install -r requirements.txt

## Documentation

I think I put most of the good stuff into `:help jiravim`, so definitely check that out for information about the commands and how to get the show on the road.

Once you got the environment set up, here is a basic workflow:

#### Basic Workflow

* Open your Kanban board with `:JiraVimBoardOpen <board name>`.
* Scroll up and down through the issues, and find one you would like to look at.
* Open the issue with `:JiraVimSelectIssueNosp`.
* Look at the issue, make notes about how wonderful your Product Manager is for writing detailed specs.
* You've had enough, you want to look at the other issues that the team must complete, so you return with `:JiraVimReturn`.

I will try to do my best to be as backward compatible as possible moving forward, but I can make no guarantees.

## Please Leave Feedback

If you do indeed try this plugin, please please please leave some feedback. I'm not the most experienced programmer, so if you have **any** comment or suggestion, either open an issue or send me an email at leonardthesalmon@protonmail.com. I will read all of your feedback (I promise).

## Contributing

Jira is a huge project, and many people use different parts of it. Doing this alone, for me, is a huge task, so I appreciate any help that comes by! 

(You still have to read this boring text first though 😞: [Contributor Guidelines](./CONTRIBUTING.md))

### Testing

The project uses the [vader.vim](https://github.com/junegunn/vader.vim) plugin for intergration testing. Run 

    vim -Nc "Vader! test/*"
 
from the project root directory. Each pull request is tested with Travis CI and Codacy as well.

## ❤️❤️❤️ If you like this ...

Please consider giving it a rating at [https://www.vim.org/scripts/script.php?script_id=5800](https://www.vim.org/scripts/script.php?script_id=5800)

And please consider contributing to the project.
