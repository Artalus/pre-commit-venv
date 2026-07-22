subjectively the best way to run some python tools from local virtualenv through
[prek](https://prek.j178.dev/) & [pre-commit](https://pre-commit.com)
---

1) Create file `.pre-commit-venv` in the root of your repo with the contents like `.venv/` or
`/git/myproject/venv` or `d:/python/my-awesome-global-venv` — wherever your virtual environment is.
2) Put the file under `.gitignore` (or at least `.git/info/exclude`).
3) Run whatever you need in your `.pre-commit-config.yaml`:
```yaml
- repo: https://github.com/Artalus/pre-commit-venv
  rev: v0.2
  hooks:
  - id: venv
    alias: mypy
    name: Run mypy from venv
    # will check everything according to mypy config (files=, packages=, ...)
    pass_filenames: false
    args: [mypy]
  - id: venv
    alias: ruff-check
    name: Run ruff check from venv
    # will check files from commit
    args: [ruff, check]
  - id: venv
    alias: ruff-format
    name: Run ruff format from venv
    args: [ruff, format, --diff]
```

> [!NOTE]
> The hook matches Python files via `types_or: [python, pyi]`


# Q&A

## Why not just ...

### ... use regular pre-commit hooks?
For every python hook, `pre-commit` installs its packages into a separate virtual environment.
This neat trick greatly simplifies usage of many tools, and occasionally allows one to use a
python-based checker in non-python codebase.
If your workflow for some tool is fine with that approach — by all means go for it.

However:
1) Some tools (*hiiii~ `mypy`*) are Notoriously Bad at handling codebases with dependencies in
venv A while the tool itself is installed into venv B:
  - https://github.com/python/mypy/issues/13916
  - https://github.com/pre-commit/pre-commit/issues/1522
  - https://github.com/pre-commit/pre-commit/issues/1580
  - https://github.com/j178/prek/issues/2349
  - many more
2) You might want to use the exact version from your environment, but maintaining the parity between
`pyproject.toml` (or any alternative) and `.pre-commit-config.yaml` is an unnecessary chore.

### ... use `repo: local` hook with and `entry: <tool>`?
This would require a virtual environment to be active when `pre-commit` runs.
Sounds like a no-issue — unless you are using VSCode or any other IDE that usually runs in its own
environment.
See https://github.com/pre-commit/pre-commit/issues/1465

### ... use `entry: .venv/bin/tool` instead then?

This would not work for us poor Windows plebs — we would have it installed as `.venv\Scripts\tool`.
:sob:

### ... commit the `.pre-commit-venv` file?

You wouldn't make a workflow-breaking tool depend on `A:/local/path` in a repo shared with other
fine folks, would you?

### ... hardcode `.venv/` path and avoid config?

Assuming that everyone would always live under `.venv/` is morally wrong.
While convention over configuration is awesome, if other devs *can* have a virtualenv named different
from `.venv/`, they *will* find a perfectly unarguable reason to do so!

### ... have `.venv/` as a default if config is missing?

Explicit requirement is better than implicit sensible default.


## Monorepos? Python projects in subfolders?

Should work as long as you can afford & keep a single common `.pre-commit-venv` file at the root
of the repo.
Separate files for different venvs are not supported.
