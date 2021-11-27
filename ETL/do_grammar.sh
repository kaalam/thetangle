#!/bin/bash

set -e


# Remove everything in all output folders

rm -rf ../../tng-data-grammar/data/gCide
rm -rf ../../tng-data-grammar/data/WordNet
rm -rf ../../tng-data-grammar/data/LinkGrammar


# Create all output folders

mkdir ../../tng-data-grammar/data/gCide
mkdir ../../tng-data-grammar/data/WordNet
mkdir ../../tng-data-grammar/data/LinkGrammar


# Setup the environment

export TANGLE_ETL_SOURCE=~/kaalam.etc/nlp/corpora


# Make raw data for Grammar

export TANGLE_ETL_DEST=../../tng-data-grammar/data

	python scripts/031_gCide.py
	python scripts/032_WordNet.py
	python scripts/033_LinkGrammar.py


# Push the github repo

etl_pwd=$(pwd)

cd ../../tng-data-grammar || return 1

./compress_clean_push.sh

cd "$etl_pwd" || return 1
