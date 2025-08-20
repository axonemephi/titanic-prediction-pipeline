#!/bin/bash

VIEW_PYTHON="/Users/smitthakkar/Desktop/functional-xoding/machine-learning-basixs/.venv/bin/python"

echo "Starting the pipeline run at $(date)"

cd /Users/smitthakkar/Desktop/functional-xoding/machine-learning-basixs/titanic-pipeline

echo "--------- Running ETL script ----------"
$VIEW_PYTHON etl.py

echo "--------- Running Prediction script ----------"
$VIEW_PYTHON predict.py

echo "Pipeline run fininshed at $(date)"