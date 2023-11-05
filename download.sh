#!/usr/bin/env bash
set -e
BASEDIR=$(dirname "$0")
cd "$BASEDIR"

mkdir -p .downloads/
cd .downloads
curl -o soc-redditHyperlinks-body.tsv https://snap.stanford.edu/data/soc-redditHyperlinks-body.tsv
curl -o soc-redditHyperlinks-title.tsv https://snap.stanford.edu/data/soc-redditHyperlinks-title.tsv
