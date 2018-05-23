#!/bin/bash

echo $options
# The %% * is a perverse trick to get first word of options, which is the job name
#SGE_Batch -r "${options%% *}" -c "python3 -u preprocess.py $options" -P 1

#SGE_Batch -r "e57-01" -c "python3 -u train.py e57-01 a:conv-3-32-in b:maxpool-1-100-a c:maxpool-100-1-a d:concat-a-b e:concat-c-d f:conv-3-32-e g:conv-3-32-f h:concat-g-in i:conv-3-5-h" -P 1
SGE_Batch -r "e59-01" -c "python3 -u train.py e59-01 a:conv-3-5-in" -P 1
SGE_Batch -r "e59-02" -c "python3 -u train.py e59-02 a:conv-3-5-in" -P 2
SGE_Batch -r "e59-04" -c "python3 -u train.py e59-04 a:conv-3-5-in" -P 4
SGE_Batch -r "e59-08" -c "python3 -u train.py e59-08 a:conv-3-5-in" -P 8
SGE_Batch -r "e59-16" -c "python3 -u train.py e59-16 a:conv-3-5-in" -P 16
SGE_Batch -r "e59-32" -c "python3 -u train.py e59-32 a:conv-3-5-in" -P 32
