<!-- This template was created to cover the most complex case of new changes to the configuration. As such, all sections may not be suitable for other types of changes (e.g. documentation changes, cherry-picking changes between configurations). Please fill in all the sections you believe are suitable to your case. The reviewer(s) will ask for any missing information. Please do not delete any empty sections. -->

**1. Summary**:

What has changed?

Why was this done?

**2. Issues Addressed:**
<!-- Add links to github issue(s) this is related to -->
-

**3. Dependencies (e.g. on payu, or model)**

This change requires changes to (note pull request where true):
- [ ] payu:
- [ ] ACCESS-ESM1.6:
- [ ] UM7:
- [ ] MOM5:
- [ ] CICE5:
- [ ] CABLE:
- [ ] GCOM4:
<!-- Describe and link to the related changes to dependencies -->

**4. Ad-hoc Testing**

What ad-hoc testing was done? How are you convinced this change is correct (plots are good)?

**5. CI Testing**
<!-- Has the CI-testing been run? -->
- [ ] `!test repro` has been run

**6. Reproducibility**

Is this reproducible with the previous commit? (If not, why not?)
- [ ] Yes
- [ ] No - `!test repro commit` has been run. <!-- add detail below for why it's answer changing -->

**8. Manifests**

Have you changed the executable, the input files and/or the restart files?
- [ ] Yes
- [ ] No

If yes, have you updated the manifests?
- [ ] Yes
- [ ] No

To update the manifests, run payu setup (in a cloned copy of your feature branch) with reproducibility tests turned off:

```yaml
manifest:
  reproduce:
    exe: false
    input: false
    restart: false
```
Then commit the newly created manifest files (under manifests/) only to the branch for this PR.


**7. Documentation**
<!--Does this impact documentation? -->

The documentation is updated?
- [ ] Yes
- [ ] N/A

**9. Merge Strategy**
<!-- What is the planned merge strategy (Merge commit, Rebase and merge, or squash) ?
If not squash, link to the related issue in the commit descriptions -->

- [ ] Merge commit
- [ ] Rebase and merge
- [ ] Squash
