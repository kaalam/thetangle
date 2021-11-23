# Python utilities for The Tangle


## What is this?

This repository contains three different parts for **building**, **testing** and **exploring** The Tangle.


## Downloading and compiling The Tangle

The complete procedure is explained [here](https://kaalam.github.io/jazz_reference/reference_docker_tangle_server.html)


## Exploring The Tangle

You can just `pip install thetangle` and run examples from the folder `python_examples`.


## Building the package

Run the script `release.sh`. You will need a `twine_credentials.sh` file that exports the system variables `TWINE_USERNAME=xxx` and
`TWINE_PASSWORD=xxx`.


## Building the datasets and pushing them to github

Setup everything (finding the sources and storing them in your staging area requires a lot of work, use the scripts in `ETL/scripts`
as a reference) and run:

```
cd ETL
./do_all.sh
```


## Integration Testing for a Jazz cluster

run `./test_cluster.sh`

You will have to set up a two node cluster and configure the IPs and ports of your nodes in `cluster_tests/http_requests.py`.
