# Branch Guidelines

Guidelines to follow when creating a branch in the Obris-CLI repo.

## Branch Prefixes

1. **Feature Branch**: Prepend branch used to develop new features with a `feature/` prefix.
1. **Bugfix Branch**: Prepend branch used to fix existing code issues with a `bugfix/` prefix.
1. **Docs Branch**: Prepend branches used to update or add documentation with a `docs/` prefix.
1. **Release Branch**: Prepend branches for new releases with a `release/` prefix.

## Include a Date

After the prefix, include the `YYYYMM` in which you created the branch.

## Seperators

Avoid using non-alphanumeric characters beyond a forward slash `/` and hyphens `-`.

* Use a forward slash `/` after the branch prefix
* Use hyphens `-` as separators between words describing the branch 

## Examples

* `feature/202312-deploy-to-webserver-clusters`
* `bugfix/202405-off-by-one-issue-in-process-assignment`
* `docs/202403-fix-typos-grammar-in-README`
