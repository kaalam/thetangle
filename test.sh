#!/bin/bash

coverage run --source=tests/ -m pytest tests/
coverage report -m
