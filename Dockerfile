FROM docker.io/python:3.9-bookworm

RUN pip install snap-stanford
RUN mkdir /data/ && wget -O /data/soc-redditHyperlinks-body.tsv https://snap.stanford.edu/data/soc-redditHyperlinks-body.tsv
# Remove first line:
#RUN sed '1d' /data/soc-redditHyperlinks-body.tsv > /tmp/tmpfile && mv /tmp/tmpfile /data/soc-redditHyperlinks-body.tsv

