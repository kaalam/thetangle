#!/bin/bash

coverage run --source=cluster_tests/ -m pytest cluster_tests/
coverage report -m
