#!/bin/bash

set -e


# Remove everything in all output folders

rm -rf ../../tng-data-raiders/data/Raiders


# Create all output folders

mkdir ../../tng-data-raiders/data/Raiders


# Setup the environment

export TANGLE_ETL_SOURCE=~/kaalam.etc/nlp/corpora


# Make raw data for Readings

export TANGLE_ETL_DEST=../../tng-data-raiders/data

	python scripts/024_RaidersOfLostKek.py


# Push all the github repos

etl_pwd=$(pwd)

cd ../../tng-data-raiders || return 1

./compress_clean_push.sh

cd "$etl_pwd" || return 1
