#!/bin/bash

rm -rf .pytest_cache
rm -rf .cache/
rm -rf .coverage
rm -rf htmlcov/
rm -f test_*.jcb
rm -f MANIFEST
rm -rf dist/
find . | grep -e '/\.pytest' | xargs rm -rf
find . | grep -e '__pycache__' | xargs rm -rf
find . | grep -e '.ipynb_checkpoints' | xargs rm -rf
find . | grep -e '.ipynb$' | xargs rm -rf
find . | grep -e '.pyc$' | xargs rm -rf
