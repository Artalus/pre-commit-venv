subjectively the best way to run some python tool through pre-commit
---

# TL;DR

1) Create file `.pre-commit-venv` in the root of your repo with the contents like `.venv/` or
`/git/myproject/venv` or `d:/python/my-awesome-global-venv` — wherever your virtual environment is.
2) Put the file under `.gitignore` (or at least `.git/info/exclude`).
3) Run whatever you need in your `.pre-commit-config.yaml`:
```yaml
- repo: https://github.com/Artalus/pre-commit-venv
  rev: 0.1
  hooks:
  - id: venv
    alias: mypy
    name: Run mypy from venv
    args: [mypy]
  - id: venv
    alias: ruff-check
    name: Run ruff check from venv
    args: [ruff, check]
  - id: venv
    alias: ruff-format
    name: Run ruff-format from venv
    args: [ruff, format, --diff]
```

> [!NOTE]
> **Q:** why ignore the file?
>
> **A:** while convention over configuration is awesome, other devs are likely to have the venv
> directory named differently.

# Why not just ...

## ... use the regular hooks?
pre-commit installs the tools for its python hooks into a separate virtual environment.
It's a really neat trick that greatly simplifies using a great bunch of different tools.
If your workflow for some tool is fine with that approach — by all means go for it.

However:
1) Some tools (hi, mypy~) are notoriously Bad at operating on a codebase requiring venv A while
tool is installed into venv B:
  - [https://github.com/python/mypy/issues/13916]
  - [https://github.com/pre-commit/pre-commit/issues/1522]
  - [https://github.com/pre-commit/pre-commit/issues/1580]
  - many more
2) You might want to use exactly the version in your environment, and maintaining the parity between
`pyproject.toml` (or any alternative) and `.pre-commit-config.yaml` is an unnecessary chore.

## ... have a `repo: local` hook with and `entry: <tool>`?
This would require a virtual environment to active at the moment when `pre-commit` runs.
Sound like a no-issue unless you are using VSCode or any other IDE that usually runs in its own environment.
https://github.com/pre-commit/pre-commit/issues/1465

## ... use `entry: .venv/bin/tool` instead then?
This would not work for the poor Windows plebs — we would have it installed as `.venv\Scripts\tool`.
Also assuming that everyone would always live under `.venv/` is morally wrong.
