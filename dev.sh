#!/bin/bash

VENV='venv'

runpy() {
    echo "Looking for main file..."
    PATH_TO_GIT=$(git rev-parse --show-toplevel)
    PATH_TO_MAIN=$(find $PATH_TO_GIT -name "venv" -prune -name ".git" -prune -or -name "__main__.py")
    echo "Main file found!"
    echo "Running main file!"
    python -u $PATH_TO_MAIN
}

activate() {
    echo "Activating virtual environment"
    source ./$VENV/Scripts/activate
    echo "To deactivate, run 'deactivate' in the terminal"
}


"$@"
