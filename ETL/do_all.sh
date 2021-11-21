#!/bin/bash

set -e


# Make all folders

mkdir -p ../../tng-data-grammar/data/indices
mkdir -p ../../tng-data-qa/data/jeopardy


# Setup the environment

export TANGLE_ETL_SOURCE=~/kaalam.etc/nlp/corpora
export TANGLE_ETL_INDICES=../../tng-data-grammar/data/indices


# Make raw data for Grammar

export TANGLE_ETL_DEST=../../tng-data-grammar/data

	# ... python scripts/031_gCide.py
	# ... python scripts/032_WordNet.py
	# ... python scripts/033_LinkGrammar.py


# Make raw data for Facts

export TANGLE_ETL_DEST=../../tng-data-facts/data

	# ... python scripts/001_ConceptNet.py
	# ... python scripts/002_Ascent.py
	# ... python scripts/003_GenericsKB.py


# Make raw data for Q&A

export TANGLE_ETL_DEST=../../tng-data-qa/data

	# ... python scripts/011_SQUAD20.py
python scripts/012_Jeopardy.py


# Make raw data for Readings

export TANGLE_ETL_DEST=../../tng-data-readings/data

	# ... python scripts/022_Gutenberg.py
	# ... python scripts/023_OpenSubtitles.py


# Make raw data for Wikipedia

export TANGLE_ETL_DEST=../../tng-data-wikipedia/data

	# ... python scripts/021_Wikipedia.py


# Create the doc and the docker upload script

	# ...


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

cd ../../tng-data-wikipedia || return 1

./compress_clean_push.sh

cd "$etl_pwd" || return 1
