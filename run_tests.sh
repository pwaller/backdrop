#!/bin/bash

set -o pipefail

function display_result {
  RESULT=$1
  EXIT_STATUS=$2
  TEST=$3

  if [ $RESULT -ne 0 ]; then
    echo -e "\033[31m$TEST failed\033[0m"
    exit $EXIT_STATUS
  else
    echo -e "\033[32m$TEST passed\033[0m"
  fi
}

if [ -z "$VIRTUAL_ENV" ]; then # not in a virtualenv
  if [ -n "$WORKON_HOME" ]; then # we are using virtualenvwrapper
    basedir=$(dirname $0)
    venvdir=$WORKON_HOME/$(basename $(cd $(dirname $0) && pwd -P))

    if [ ! -d "$venvdir" ]; then
      virtualenv $venvdir
    fi

    source "$venvdir/bin/activate"
  else
    # not in a virtualenv and not using virtualenvwrapper
    echo -e "\033[31mError: Unable to run tests - must activate virtualenv\033[0m"
    exit 1
  fi
fi


pip install -r requirements_for_tests.txt

rm -f coverage.xml .coverage nosetests.xml
find . -name '*.pyc' -delete

# run unit tests
nosetests -v --with-xunit --with-coverage --cover-package=backdrop
display_result $? 1 "Unit tests"

# create coverage report
python -m coverage.__main__ xml --include=backdrop*

# run feature tests
behave --stop --tags=~@wip --tags=~@file_upload_test
display_result $? 2 "Feature tests"

# run style checks
./pep-it.sh | tee pep8.out
display_result $? 3 "Code style check"

