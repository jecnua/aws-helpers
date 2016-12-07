#!/bin/bash

python autoscaling/metrics/check_enabled_metrics_for_ag.py
python autoscaling/diff/check_autoscaling.py
python autoscaling/process/check_autoscaling.py
