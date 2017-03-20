# Collection of scripts

This repo contains a collection of script to help with basic AWS administration.
All directories cover a service or topic and you can find a README (hopefully)
in each of them :)

## Disclaimers

I am not a python developer and the code is sure as hell not so good, but it
does the job. :D

## Requirements

There are Requirements file in every directory.
You can install the python dependencies via:

    pip install -r requirements.txt

## Env

- Python3

## Linted automatically

    autopep8 --in-place autoscaling/metrics/*.py
    autopep8 --in-place autoscaling/diff/*.py
    autopep8 --in-place autoscaling/process/*.py
