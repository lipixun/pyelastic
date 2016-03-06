#!/bin/bash
# Build the artifact

SDISTDIR=./dist
DEPFILE=dependency
CONFIGDIR=config

# Get the full name
VERSION=`python setup.py --version`
if [[ $VERSION == '' ]]; then
    echo Package version not found >&2
    exit 1
fi

echo Build package $VERSION

# Run python setup, this will generate a tgz file in ./dist directory with name name-version.tar.gz
python setup.py sdist -d $SDISTDIR
if [[ $? != 0 ]]; then
    echo Failed to build package >&2
    exit 1
fi

# Write package files
PACKAGEFILE=`python setup.py --fullname`
PACKAGEFILE=$PACKAGEFILE.tar.gz

echo $PACKAGEFILE >$SDISTDIR/packages

# Write version file
echo $VERSION > $SDISTDIR/version

# Copy dependency definitions
if [[ -f $DEPFILE ]]; then
    cp $DEPFILE $SDISTDIR/
    if [[ $? != 0 ]]; then
        echo Failed to copy dependency file >&2
        exit 1
    fi
fi

# Copy configurations
if [[ -d $CONFIGDIR ]]; then
    cp -r $CONFIGDIR $SDISTDIR/
    if [[ $? != 0 ]]; then
        echo Failed to copy config >&2
        exit 1
    fi
fi

