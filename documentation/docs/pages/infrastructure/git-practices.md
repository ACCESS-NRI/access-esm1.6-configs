# Git practices

## Automated Cherry Picking

There is a workflow which enables semi-automated cherry-picking from one branch into another, using the !cherry-pick keyword in a pull-request. This is useful when changes need to be applied across multiple branches.

For example, if you have made a pull request into `dev-piControl` and want to duplicate the changes in `dev-esm-piControl`:
1. Finalise and merge the pull request into `dev-piControl`.
2. Identify the newly created commits in `dev-piControl` which you want to copy over to `dev-esm-piControl`, e.g. `hash1`, `hash2`, ..., `hashn`. This could be all, or just a subset of the commits created by merging the PR, depending on which specific changes you want to copy over. Omit any merge commits from this list, as they are not supported by the automatic cherry pick command.
3. In a new comment in the just merged PR, use the `!cherry-pick` command as follows:
    `!cherry-pick hash1 hash2 <...> hashn into dev-esm-piControl`

This will create a new PR into `dev-esm-piControl` which adds the requested commits, and it will leave a comment on the initial PR with the outcome of the command.


!!! warning

    The selected commits must exist in the base branch of the PR where the `!cherry-pick` command is run. In the above example, the command will fail if the commits don't exist in `dev-piControl`. For this reason, you must merge the initial PR before using the `!cherry-pick` command.

!!! warning

    In the case where the initial PR is answer changing, we recommend the following approach. First organise your changes into a neat set of commits, and then run the `!test repro commit` command. Merge the PR using the `Create a merge commit` option rather than the `Squash and merge` option, which will keep the main content of the PR separate from the checksum changes. Finally, identify the newly created non-checksum commits in the the base branch, and use these in the `!cherry-pick` comment command.