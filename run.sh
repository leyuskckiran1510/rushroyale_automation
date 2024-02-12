#!/usr/bin/bash

# this script is for replacing Makefile
# run this in gitbash if you are windows user



all() {
    if [[ ! -d "virtual" || $1 == "force" ]]; then
        echo "Creating Virtual Environment..."
        python -m venv virtual || {
            echo "Error: Failed to create virtual environment."
            return 1
        }
    fi

    echo "Activating the Virtual Environment [virtual]..."
    source ./virtual/Scripts/activate || {
        echo "Error: Failed to activate virtual environment."
        return 1
    }

    echo "Virtual Environment [virtual] is activated."

    if [[ -f "requ.txt" ]]; then
        echo "Installing dependencies from [requ.txt]..."
        python -m pip install -r ./requ.txt || {
            echo "Error: Failed to install dependencies."
            return 1
        }
        echo "Dependency installation completed."
    else
        echo "Warning: No 'requ.txt' file found. Skipping dependency installation."
    fi

    if [[ -n "$VIRTUAL_ENV" ]]; then
        python ./src/main.py "$@"
    else
        echo "Error: Failed to set up the environment or install dependencies."
    fi
}
 

runc(){
   c_code && ./a.exe
}
c_code(){
    gcc ./src/main.c -o a.exe -luser32
}

case $1 in
    'runc') runc $@ ;;
    *) all $@;;
esac