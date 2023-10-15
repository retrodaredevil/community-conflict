# community-conflict
A social network analysis of how different subreddits interact with each other

## Virtual Env Setup

### Linux

```shell
# make sure venv is installed
sudo apt install python3-venv

./setup_venv.sh

sudo docker build --tag community-conflict . && sudo docker run -v "$(pwd)/test.py:/data/test.py:ro" --rm -it community-conflict
```

## Playing with the table

Get into an interactive Python environment (likely by running the docker command), then do this:

```python
>>> exec(open("/data/test.py").read())
>>> table
<snap.PTable; proxy of <Swig Object of type 'TPt< TTable > *' at 0x7f5e6f9fa9f0> >
```

## Understanding `snap-stanford` library compatibility
Take this command: `sudo docker run --rm -it python:3.10-bookworm python -m pip install snap-stanford`.
As of 2023-10-14, it will fail.
You can see this issue here: https://github.com/snap-stanford/snap-python/issues?q=%22Could+not+find+a+version+that+satisfies+the+requirement+snap-stanford%22

As of right now, Python 3.9 is the highest supported version of Python for snap-stanford.
