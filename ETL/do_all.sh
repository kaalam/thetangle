#!/bin/bash

set -e


# Remove everything in all output folders

rm -rf ../../tng-data-facts/data/ConceptNet
rm -rf ../../tng-data-facts/data/ascent
rm -rf ../../tng-data-facts/data/GenericsKB
rm -rf ../../tng-data-grammar/data/gCide
rm -rf ../../tng-data-grammar/data/WordNet
rm -rf ../../tng-data-grammar/data/LinkGrammar
rm -rf ../../tng-data-qa/data/squad20
rm -rf ../../tng-data-qa/data/jeopardy
rm -rf ../../tng-data-readings/data/OpenSubtitles
rm -rf ../../tng-data-readings/data/gutenberg
rm -rf ../../tng-data-raiders/data/Raiders
rm -rf ../../tng-data-wikipedia/data/wikipedia


# Create all output folders

mkdir ../../tng-data-facts/data/ConceptNet
mkdir ../../tng-data-facts/data/ascent
mkdir ../../tng-data-facts/data/GenericsKB
mkdir ../../tng-data-grammar/data/gCide
mkdir ../../tng-data-grammar/data/WordNet
mkdir ../../tng-data-grammar/data/LinkGrammar
mkdir ../../tng-data-qa/data/squad20
mkdir ../../tng-data-qa/data/jeopardy
mkdir ../../tng-data-readings/data/OpenSubtitles
mkdir ../../tng-data-readings/data/gutenberg
mkdir ../../tng-data-raiders/data/Raiders
mkdir ../../tng-data-wikipedia/data/wikipedia


# Setup the environment

export TANGLE_ETL_SOURCE=~/kaalam.etc/nlp/corpora


# Make raw data for Grammar

export TANGLE_ETL_DEST=../../tng-data-grammar/data

	python scripts/031_gCide.py
	python scripts/032_WordNet.py
	python scripts/033_LinkGrammar.py


# Make raw data for Facts

export TANGLE_ETL_DEST=../../tng-data-facts/data

	python scripts/001_ConceptNet.py
	python scripts/002_Ascent.py
	python scripts/003_GenericsKB.py


# Make raw data for Q&A

export TANGLE_ETL_DEST=../../tng-data-qa/data

	python scripts/011_SQUAD20.py
	python scripts/012_Jeopardy.py


# Make raw data for Readings

export TANGLE_ETL_DEST=../../tng-data-readings/data

	python scripts/022_Gutenberg.py
	python scripts/023_OpenSubtitles.py

export TANGLE_ETL_DEST=../../tng-data-raiders/data

	python scripts/024_RaidersOfLostKek.py


# Make raw data for Wikipedia

export TANGLE_ETL_DEST=../../tng-data-wikipedia/data

	python scripts/021_Wikipedia.py


# Push all the github repos

etl_pwd=$(pwd)

cd ../../tng-data-grammar || return 1

./compress_clean_push.sh

cd "$etl_pwd" || return 1

etl_pwd=$(pwd)

cd ../../tng-data-facts || return 1

./compress_clean_push.sh

cd "$etl_pwd" || return 1

etl_pwd=$(pwd)

cd ../../tng-data-qa || return 1

./compress_clean_push.sh

cd "$etl_pwd" || return 1

etl_pwd=$(pwd)

cd ../../tng-data-readings || return 1

./compress_clean_push.sh

cd "$etl_pwd" || return 1

etl_pwd=$(pwd)

cd ../../tng-data-raiders || return 1

./compress_clean_push.sh

cd "$etl_pwd" || return 1

etl_pwd=$(pwd)

cd ../../tng-data-wikipedia || return 1

./compress_clean_push.sh

cd "$etl_pwd" || return 1
