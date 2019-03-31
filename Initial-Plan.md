# Initial plan

This is the initial plan document of how this is gonna work.

### Jira Integration

I plan to have all Jira integration go with [Basic Authentication](https://developer.atlassian.com/server/jira/platform/basic-authentication/) for now. OAuth2 is an option once we get this working. See the Security section for more details on the authentication process.

Requests themselves will go through the Vim Python interface. I think it's reasonable to expect most modern systems to have python installed.

#### Security
Credentials will be stored in global variables (this might need more thought) and will be accessed by the plugin to authenticate requests.
