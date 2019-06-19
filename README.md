# jira-vim

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/5d3c5f54a99b44688ea474d3b0a3fba7)](https://app.codacy.com/app/paul.kassianik/jira-vim?utm_source=github.com&utm_medium=referral&utm_content=paulkass/jira-vim&utm_campaign=Badge_Grade_Settings)

A vim plugin to access your Jira workspace directly from Vim

## Current Stage: Writing the code!!

I'm currently writing the code for this project. My goal for the first release (or stage) is to have the app display information properly and easily. I'm also trying to make it easy for users to not only modify the app easily to suit their needs, but also to contribute to the project. Information on my immediate goals can be found here: [Project Page](https://github.com/paulkass/jira-vim/projects/1).

If you do indeed try this plugin, please please please leave some feedback. I'm not the most experienced programmer, so if you have **any** comment or suggestion, either open an issue or send me an email at leonardthesalmon@protonmail.com. I will read all of your feedback (I promise).

## Dependencies on other Vim Plugins

The default formatting uses [Tabularize](https://github.com/godlygeek/tabular). To put it in your plugin manager, add 
```vimscript
Plug 'godlygeek/tabular'
```

## Dependencies on Python

Please compile Vim with python3 for this plugin to function properly.

Then install the `requirements.txt` file with pip.
