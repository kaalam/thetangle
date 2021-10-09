#!/bin/bash

rm -rf *.pyc
rm -rf .ipynb_checkpoints/
rm -rf .pytest_cache
rm -rf .cache/
rm -rf .coverage
rm -rf htmlcov/
rm -f *.ipynb
rm -f test_*.jcb
rm -f MANIFEST
rm -rf dist/
find . | grep -e '/\.pytest' | xargs rm -rf
find . | grep -e '__pycache__' | xargs rm -rf
