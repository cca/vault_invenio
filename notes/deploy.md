# Deployment

https://inveniordm.docs.cern.ch/deploy/

https://github.com/inveniosoftware/helm-invenio

https://discord.com/channels/692989811736182844/1034787528735215628

## GitLab Mirroring

We mirror [the GitHub repo](https://github.com/cca/vault_invenio/) to GitLab where we run CI/CD. To set up the mirroring:

1. Create a fine-grained personal access token under settings > [tokens](https://github.com/settings/tokens).
    1. Set expiration for one year and create a reminder sometime before that date to rotate the token
    1. **Resource owner** will be CCA and not your personal account. CCA appears as an option here because under CCA > settings > [Personal access tokens](https://github.com/organizations/cca/settings/personal-access-tokens) we allow access to org repos via fine-grained access tokens
    1. **Only select repositories** = Invenio repo
    1. Permissions > Repository permissions > **Read-only** access to **Commit statuses** and **Contents**. Metadata read access should be on by default.[^1]
    1. Generate the token, copy it, store it in Dashlane and share with relevant folks
1. Under Invenio repo > Settings > [Collaborators and teams](https://github.com/cca/vault_invenio/settings/access) add your account as an admin (otherwise repo will not show up under Collaborators list on GitLab)
1. If setting up mirroring for the first time... (not needed if rotating tokens, see below)
    1. Create a project on GitLab and choose "Run CI/CD for external repository"
    1. Select **GitHub** and paste your token
    1. Under the **Collaborated** repos tab, find the Invenio GitHub repo
    1. Under the **To GitLab** column, select the CCA organization rather than your personal account
    1. **Connect** it to GitLab. The first time, the status indicator on this page never finished, but the Invenio repo did appear under the CCA org on GitLab.
1. Rotating token: go to Invenio repo on GitLab > Integrations > Configure the [GitHub Integration](https://gitlab.com/california-college-of-the-arts/invenio/-/settings/integrations/github/edit) and enter the new token

[^1]: Eric asked GitLab exactly what permissions their integration needs here but their response did not make sense. It's possible the permissions needed will change over time. They said "GitLab doesn't test against fine-grained permissions on GitHub's access tokens so there may be additional adjustments required if you want to use a fine-grained access token. If there are any access issues there will be a logged error message that explains what additional permissions are needed."
