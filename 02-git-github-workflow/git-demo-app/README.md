# 🛠️ Git & GitHub Complete Workflow Demonstration App

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Git Workflow](https://img.shields.io/badge/Git-Feature%20Branching-orange.svg)](https://git-scm.com/)

A hands-on Python project built and managed entirely through Git in VS Code, demonstrating industry-standard version control practices, feature branching strategies, conventional commits, and remote repository synchronization.

---

## 📌 Project Overview

This sub-project demonstrates the end-to-end Git and GitHub development workflow:

- **Comprehensive `.gitignore` Configuration**: Safeguards sensitive credentials (`.env`), virtual environments (`.venv`), and bytecode caches (`__pycache__`).
- **Multi-Branch Development**: Isolated feature branches (`feature-multiply` and `feature-divide-docs`) merged back into `main`.
- **Atomic Conventional Commit Log**: Structured commit history with 5+ conventional commits.
- **GitHub Sync**: Remote tracking, branch pushing, and pull request workflows.

---

## 🛠️ System Requirements & Environment

- **Operating System:** Windows 10/11, macOS, or Linux
- **Code Editor:** Visual Studio Code / PyCharm
- **Shell:** Git Bash / PowerShell / Terminal
- **Runtime:** Python 3.8+
- **Version Control:** Git 2.x+

---

## 🚀 Core Git Command Reference

| Command | Purpose in Workflow |
|---|---|
| `git init` | Initialized the local Git repository |
| `git status` | Checked working tree status and staging area |
| `git add` | Staged untracked and modified files |
| `git commit` | Created snapshots with descriptive commit messages |
| `git log` | Inspected commit history (`--oneline --graph --all`) |
| `git branch` | Listed and created feature branches |
| `git switch` | Switched between `main` and active feature branches |
| `git diff` | Inspected unstaged code changes prior to committing |
| `git remote` | Linked and inspected remote GitHub origin |
| `git push` | Published local commits and feature branches to GitHub |
| `git pull` | Synchronized updates from remote repository to local workspace |

---

## 🌿 Branching & Commit Graph Visualizer

```text
* 4a1b2c3 (HEAD -> main, origin/main) chore: add version docstring to app module
*   3f8e9d2 Merge branch 'feature-divide-docs'
|\  
| * 2b7c6a1 (feature-divide-docs) feat: implement division logic and add project documentation
|/  
*   1c9d8e7 Merge branch 'feature-multiply'
|\  
| * 0a8b7c6 (feature-multiply) feat: add multiplication feature on feature-multiply branch
|/  
* 9e8d7c6 feat: add basic arithmetic operations
* 8d7c6b5 feat: initial commit with app base and .gitignore
```

### Commit Log Summary

1. **Commit 1:** `feat: initial commit with app base and .gitignore` (Base layout & protection rules).
2. **Commit 2:** `feat: add basic arithmetic operations` (Implemented `add` and `subtract` on `main`).
3. **Commit 3:** `feat: add multiplication feature on feature-multiply branch` (Created branch, implemented `multiply`, merged into `main`).
4. **Commit 4:** `feat: implement division logic and add project documentation` (Created branch, implemented safe division + documentation, merged into `main`).
5. **Commit 5:** `chore: add version docstring to app module` (Module docstrings and final polish).

---

## 🔒 Security & Ignored Files (`.gitignore`)

The repository enforces strict exclusion rules via `.gitignore`:

- **Virtual Environments:** `venv/`, `.venv/`, `env/`
- **Secrets & Credentials:** `.env`, `*.env`, `secrets.json`, `*.pem`, `*.key`
- **Bytecode & Caches:** `__pycache__/`, `*.pyc`
- **IDE Metadata:** `.vscode/`, `.idea/`

---

## 💻 Running the Application Locally

1. Navigate to the demo app directory:

```bash
cd 02-git-github-workflow/git-demo-app
```

2. Run the application script:

```bash
python app.py
```

### Sample Output:
```text
=== Git Demo Application ===
5 + 3 = 8
10 - 4 = 6
6 * 7 = 42
20 / 4 = 5.0
```
Demonstrated live for evaluation.
