#!/bin/bash
# Run the test for artifact, this is always called build verification test

BUILD_TEST_FILE=./test/buildtest/test.py

if [[ -f $BUILD_TEST_FILE ]]; then

    echo Run build verification test >&2
    pip install -r requirements.txt && pip install -r requirements4test.txt
    if [[ $? != 0 ]]; then
        echo Failed to install prerequests >&2
        exit 1
    fi

    # Run test
    nosetests $BUILD_TEST_FILE
    exit $?

else

    echo No test found >&2

fi

