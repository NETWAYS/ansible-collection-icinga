# Creating a new release

> This is meant as an *internal* note on how to build and publish a new version of this Ansible Collection.

1. **Get the release branch ready:**<br>
   Push your local changes to the remote.<br>
   From your local release branch:<br>
   ```bash
   git push --set-upstream origin release/<VERSION>
   ```

   To avoid having leftover files from your local directory end up in the release, please **cleanly clone the release branch to another directory**.<br>
   ```bash
   git clone --branch release/<VERSION> git@github.com:NETWAYS/ansible-collection-icinga.git release_<VERSION>
   cd release_<VERSION>
   ```
   You now only have files that were actually commmited.<br>

2. **Increase the version number:**<br>
   The version of this Collection - as seen by Ansible Galaxy - is determined by **galaxy.yml**.<br>
   Increase the version number inside accordingly.<br>

3. **Create a changelog summary:**<br>
   This will be shown in the changelog as a short summary for this release.<br>

   changelogs/fragments/release_summary.yml:<br>
   ```yaml
   release_summary: |
     Summary text for this release.
     "*Bugfix release*" for example.
   ```

4. **Create a new changelog:**<br>

   Lint the changelogs:<br>
   ```bash
   antsibull-changelog lint
   ```

   Generate the changelog:<br>
   ```bash
   antsibull-changelog release --version <VERSION>
   ```

   Commit your changes to the release branch.

5. **Build and push to Ansible Galaxy:**<br>

   Build a release tar ball (verbose shows skipped files):<br>
   ```bash
   ansible-galaxy collection build -vvv
   ```

   Push to Ansible Galaxy:<br>
   ```bash
   ansible-galaxy collection publish --token <TOKEN> netways-icinga-<VERSION>.tar.gz
   ```
   > This might show errors which does **not** necessarily mean that it failed.<br>
   > Have a look at [Ansible Galaxy](https://galaxy.ansible.com/ui/repo/published/netways/icinga/) and confirm if the release could be published.

6. **Create a release on GitHub:**<br>
   When [creating a new release](https://github.com/NETWAYS/ansible-collection-icinga/releases/new)<br>

   - choose \<VERSION\> as tag
   - choose the branch "release/\<VERSION\>" as target (will be tagged)
   - choose \<VERSION\> as title
   - copy and paste the release's changelog entry (see [prior releases](https://github.com/NETWAYS/ansible-collection-icinga/releases))
   - attach the created tar ball (netways-icinga-\<VERSION\>.tar.gz) to the release
   - if you feel extra nice, credit contributors by adding their names, e.g. behind the respective issue or feature (`@name`)
