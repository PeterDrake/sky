#!/bin/bash
while read options; do echo $options; export options; sbatch run.sh; done <conditions.txt

