#!/usr/bin/env bash
set -e
BASEDIR=$(dirname "$0")
cd "$BASEDIR"

mkdir -p .downloads/
cd .downloads
wget https://snap.stanford.edu/data/soc-redditHyperlinks-body.tsv
wget https://snap.stanford.edu/data/soc-redditHyperlinks-title.tsv
