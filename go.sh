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
        ut)
            export TASKS='ut'
            shift
            ;;
        ft)
            export TASKS='ft'
            shift
            ;;
        js)
            export TASKS='jsTest'
            shift
            ;;
        *)
            export ARG="$1"
            break
            ;;
    esac
done

if [ ! "$SETTINGS_FILE" == "" ]
then
    echo "Using settings file - $SETTINGS_FILE"
fi

if [ "$TASKS" ==  "" ]
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
        jsTest)
            echo "running js tests"
            ./node_modules/karma/bin/karma start
            ;;
        ut)
            echo "running unit tests"
            echo "Testing $ARG"
            if [ -a $SETTINGS_FILE ]
            then
                ./manage.py test --settings=$SETTINGS_FILE $ARG
            else
                ./manage.py test $ARG
            fi
            ;;
        ft)
            echo "running functional tests"
            echo "Testing $ARG"
            if [ -a $SETTINGS_FILE ]
            then
                ./manage.py harvest --tag=-WIP --tag=-Upload -v 2 --settings=$SETTINGS_FILE $ARG
            else
                ./manage.py harvest --tag=-WIP --tag=-Upload $ARG
            fi
            ;;
    esac
done
