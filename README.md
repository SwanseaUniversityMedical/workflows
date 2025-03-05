# workflows
Reusable CI/CD workflows and actions for the Organization.

## Repo structure

Reusable actions and workflows can be found under the `.github` directory. 

In the workflows directory there are both reusable workflows, workflows which run those workflows on this repo, and workflows which manage versioning and releasing all the other workflows and actions in this repo.

```
.github/
  actions/
    <asset>/**                             # A reusable action that can be invoked across the org
    
  workflows/
    <asset>.yaml                            # A reusable workflow that can be invoked across the org
    workflows-<asset>.yaml                  # Runs a reusable workflow on this repo
    workflows-release-<asset>-action.yaml   # Versions and releases an action
    workflows-release-<asset>-workflow.yaml # Versions and releases a reusable workflow
```
