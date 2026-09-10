# Contributing
A roadmap of this project is located at https://github.com/NETWAYS/ansible-collection-icinga/milestones. Please consider
this roadmap when you start contributing to the project.

Before starting your work on this module, you should [fork the project] to your GitHub account. This allows you to
freely experiment with your changes. When your changes are complete, submit a [pull request]. All pull requests will be
reviewed and merged if they suit some general guidelines:

* Changes are located in a topic branch
* For new functionality, proper tests are written
* Changes should not solve certain problems on special environments

## Changelog fragments

This repository uses [Ansible Changelogs Fragments]. A basic changelog fragment is a .yaml or .yml file placed in the changelogs/fragments/ directory. Each file contains a yaml dict with keys like bugfixes or major_changes followed by a list of changelog entries of bugfixes or features.

Each PR must use a new fragment file rather than adding to an existing one, so we can trace the change back to the PR that introduced it. Example:

```yaml
# cat changelogs/fragments/fix_issue_123.yml
---
bugfixes:
  - Fixes issue with something that was caused by something else
```

## Branches
Choosing a proper name for a branch helps us identify its purpose and possibly find an associated bug or feature.
Generally a branch name should include a topic such as `fix` or `feature` followed by a description and an issue number
if applicable. Branches should have only changes relevant to a specific issue.

```bash
git checkout -b fix/service-template-typo-1234
git checkout -b feature/config-handling-1235
git checkout -b doc/fix-typo-1236
```

## Testing
Python modules are unit tested with the Python Standard Library. For integration tests we use [Molecule]. When modifying
existing modules or tasks, make sure all existing tests pass. If you add new functionality, make sure to write appropriate
tests as well.

[fork the project]: https://help.github.com/articles/fork-a-repo/
[pull request]: https://help.github.com/articles/using-pull-requests/
[Molecule]: https://github.com/ansible-community/molecule/
[Ansible Changelogs Fragments]: https://docs.ansible.com/ansible/latest/dev_guide/developing_collections_changelogs.html
