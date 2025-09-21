# zipline-env-builder 
A simple and powerful CLI tool to automate the setup of isolated backtesting environments for zipline-reloaded.

## The Problem
Setting up a new backtest environment for a trading algorithm is often a manual, time-consuming, and error-prone process. An engineer typically has to:

Manually create a new Python virtual environment.

Remember and install the correct versions of zipline-reloaded and all its dependencies.

Copy over their algorithm script and necessary data configurations.

Write a small script just to run the backtest.

This leads to inconsistent environments across a team, making it difficult to reproduce results. It's a classic case of engineering "toil"—low-value, repetitive work that should be automated. zipline-env-builder solves this by providing a single command to get a ready-to-use, isolated backtesting environment.

## Features 
CLI First: A simple and intuitive command-line interface for ease of use.

Isolated Environments: Automatically creates a self-contained Python virtual environment using venv to prevent dependency conflicts.

Reproducible Builds: Reliably installs a specific version of zipline-reloaded and its dependencies to ensure consistent results every time.

Automated Scaffolding: Copies the user's strategy file and generates a ready-to-use run_backtest.sh script.

User-Friendly Feedback: Provides clear status messages during the setup process so you know exactly what's happening.
