# Git practices

## Automated Cherry Picking

There is a workflow which enables semi-automated cherry-picking from one branch into another, using the !cherry-pick keyword in a pull-request. This is useful when a change needs to be applied across multiple branches.

For example, if a pull-request changes `dev-piControl`, to apply the change to `dev-esm-piControl`:
- First finalise and merge the pull-request into `dev-piControl`.
- Second, as a standalone comment in the pull-request, use the keyword as follows:
    ` !cherry-pick <commit> into <branch> `

\<commit> must exist in `dev-piControl`. This can be one or multiple commit hashes seperated by spaces.
\<branch> would be `dev-esm-piControl` in this example

This will attempt to make a new pull-request with the request commit(s), and leave a comment on the initial-pull request with the outcome.

!!! warning

    In the case where the PR is answer changing, it's recomended to organise your changes into a neat set of commits prior to using the `!test repro commit` command. When merging, select `Create a merge commit` rather than `Squash and merge`, as this will allow you to select just the non-checksum commits in the `!cherry-pick` comment command.
