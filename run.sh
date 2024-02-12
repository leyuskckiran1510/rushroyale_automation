#!/usr/bin/bash

set -x 
# this script is for replacing Makefile
# run this in gitbash if you are windows user

install_dependency(){
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

}

activate_venv(){
    if [[ ! -d "virtual" || $1 == "force" ]]; then
        echo "Creating Virtual Environment..."
        python -m venv virtual || {
            echo "Error: Failed to create virtual environment."
            return 1
        }
        install_dependency || {
            echo "Failed To install dependency Please use 'force' next time"
        }
    fi

    if [[ -z "$VIRTUAL_ENV" ]]; then
        echo "Activating the Virtual Environment [virtual]..."
        source ./virtual/Scripts/activate || {
            echo "Error: Failed to activate virtual environment."
            return 1
        }
    fi

    echo "Virtual Environment [virtual] is activated."

}

all() {
    
    activate_venv $@
    
    if [[ -n "$VIRTUAL_ENV" ]]; then
        python ./src/main.py "$@"
    else
        echo "Error: Failed to set up the environment or install dependencies."
    fi
}
 

runc(){
   c_code && ./a.exe
}

prepdll(){
    gcc ./src/main.c -shared -o mouse_click.dll  -luser32   
}
c_code(){
    gcc ./src/main.c -o a.exe -luser32
}

case $1 in
    'runc') runc $@ ;;
    'prepdll') prepdll $@;;
    *) all $@;;
esac