# jira-vim

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/5d3c5f54a99b44688ea474d3b0a3fba7)](https://app.codacy.com/app/paul.kassianik/jira-vim?utm_source=github.com&utm_medium=referral&utm_content=paulkass/jira-vim&utm_campaign=Badge_Grade_Settings)

Jira-vim is a way to view your JIRA setup without the bloat of the JIRA UI.

Imagine browsing Jira on your computer. All those buttons, animations, and
fancy UI magic that you don't really need are really slowing down your
computer. It's not improving your productivity, on the contrary it makes you
wait and distract yourself while it loads features you'll never need! So I
created this: an attempt at de-bloating Jira by getting rid of the UI and using
the standard Vim environment that we know and love to display data that we
obtain from the API. 

## Current Status: Preparing for the Alpha release!!

Now that the basics are down, it's time to clean up for the alpha release. That means prettyfying things, simplifying stuff that can be automated fairly easily, and adding more information to places that were previously stubs or placeholders. You can view my progress on this [milestone](https://github.com/paulkass/jira-vim/milestone/1).

## Installation

With Pathogen, use:

    cd ~/.vim/bundle
    git clone https://github.com/paulkass/jira-vim

With Vim-Plug, use:

    Plug 'paulkass/jira-vim'

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

## Dependencies on Python

Please compile Vim with python3 for this plugin to function properly.

Then install the `requirements.txt` file with pip.

## Please Leave Feedback

If you do indeed try this plugin, please please please leave some feedback. I'm not the most experienced programmer, so if you have **any** comment or suggestion, either open an issue or send me an email at leonardthesalmon@protonmail.com. I will read all of your feedback (I promise).

