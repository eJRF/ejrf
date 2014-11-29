#!/bin/bash
set -e

while test $# -gt 0; do
    case "$1" in
        -h|--help)
            echo "run with no arguments to run everything"
            exit 0
            ;;
        --tasks*)
            export TASKS=`echo $1 | sed -e 's/^[^=]*=//g'`
            shift
            ;;
        --settings*)
            export SETTINGS_FILE=`echo $1 | sed -e 's/^[^=]*=//g'`
            shift
            ;;
        --venv*)
            export VENV=`echo $1 | sed -e 's/^[^=]*=//g'`
            shift
            ;;
        *)
            break
            ;;
    esac
done

if [ -a $TASKS ]
then
    export TASKS='setup','migrate','ut','ft'
fi

if [ ! -a $VENV ]
then
    echo "setting venv"
    source $VENV
fi

arr=$(echo $TASKS | tr "," "\n")

for x in $arr
do
    case $x in
        setup)
            echo "running setup"
            pip install -r pip-requirements.txt
            pip install coveralls
            ;;
        migrate)
            echo "running migrations"
            ./manage.py syncdb --noinput
            ./manage.py migrate
            ;;
        ut)
            echo "running unit tests"
            if [ -a $SETTINGS_FILE ]
            then
                ./manage.py test --settings=$SETTINGS_FILE
            else
                ./manage.py test
            fi
            ;;
        ft)
            echo "running functional tests"
            if [ -a $SETTINGS_FILE ]
            then
                ./manage.py harvest --tag=-WIP --tag=-Upload -v 2 --settings=$SETTINGS_FILE
            else
                ./manage.py harvest --tag=-WIP --tag=-Upload -v 2
            fi
            ;;
    esac
done
