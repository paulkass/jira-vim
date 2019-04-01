# Initial plan

This is the initial plan document of how this is gonna work.

## Jira Integration

I plan to have all Jira integration go with [Basic Authentication](https://developer.atlassian.com/server/jira/platform/basic-authentication/) for now. OAuth2 is an option once we get this working. See the Security section for more details on the authentication process.

Requests themselves will go through the Vim Python interface. I think it's reasonable to expect most modern systems to have python installed.

#### Security
Credentials will be stored in global variables (this might need more thought) and will be accessed by the plugin to authenticate requests. The problem with this setup might be that other plugins can access the credentials. Another possiblity is OAuth, but that seems like it will require more action on the user's part [OAuth Authentication for REST API's](https://developer.atlassian.com/server/jira/platform/oauth/).


## Design of Python Component

#### Class Design

TODO

#### Bundling

TODO


## Display Format 

The primary goal should be the ability to load, display, and edit jira Issues. So for now we only need two main view formats:
* Board view
* Issue view

#### Board View

The Board view will show the board for particular project. The format will contain sections for every "Column" and every line will contain an issue header with some infomation. I'm planning to later add a vertical layout more akin to the layout native to Jira, so the possibility of extension of the layout should be considered when writing code. Every issue line should be able to lead the Issue view for that particular issue. The line of the cursor will be highlighted. It will have the `jiraboarview` filetype and have a special syntax highlight.

#### Issue View

The Issue view will contain all information about the jira issue in question. Fields with editable custom text will have unmodifiable headers, e.g. 

    Title: Sample Text
    Description: This is a sample issue that needs to be fixed

where the `Title: ` and `Description: ` would not be removable with normal vim commands. The only way to remove an optional field would be through a separate mapping. These headers would also be syntax highlighted, and special Vim Sections would be applied to this type of buffer. I'm looking to optimize the approach in [this vim plugin for forms](https://github.com/tomtom/vimform_vim).

For fields that have predefined value options (like `Priority` or `Assignee`) will have dropdowns a la [Neocomplete](https://github.com/Shougo/neocomplete.vim) or [YouCompleteme](https://github.com/Valloric/YouCompleteMe). In fact, the latter is written in python so it might be better for this particular project.

## Issue Loading

The issue of loading (see what I did there?) is that it will probably be inefficient to reload the issue every time it's displayed. Therefore there are a couple of options I came up with to improve loading:
* Caching
* Partial Loading 
* Pre-Loading

#### Caching

This would involve keeping the last 5-10 issues loaded by the users in a cache somewhere (say `/tmp/jira-vim-cache`). A command to manually check for changes and (with the `!` flag reload them into the current buffer) should be added in this case.

#### Partial Loading

This would particularly work well with neovim. Since the Jira API supports expandable loading [Expansion, pagination, and ordering](https://developer.atlassian.com/cloud/jira/platform/rest/v3/?utm_source=%2Fcloud%2Fjira%2Fplatform%2Frest%2F&utm_medium=302#expansion), we could load the basic parts of an issue first and load the rest as required.

#### Pre-Loading

This is similar to caching, and again would work amazingly with neovim. The idea would be to assume (using some heuristic) which issues are likely to be loaded next and pre-load them into the cache so that they are reloaded again when called upon.

I'm more inclined towards Partial loading since it integrates well with the design of the Jira API.
