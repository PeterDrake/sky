#!/bin/bash

echo $options
# The %% * is a perverse trick to get first word of options, which is the job name
#SGE_Batch -r "${options%% *}" -c "python3 -u preprocess.py $options" -P 1

SGE_Batch -r "e55-00-08" -c "python3 -u train.py e55-00-08 a:conv-3-32-in b:maxpool-1-100-a c:maxpool-100-1-a d:concat-a-b e:concat-c-d f:conv-3-32-e g:conv-3-32-f h:concat-g-in i:conv-3-5-h" -P 8
SGE_Batch -r "e55-00-16" -c "python3 -u train.py e55-00-16 a:conv-3-32-in b:maxpool-1-100-a c:maxpool-100-1-a d:concat-a-b e:concat-c-d f:conv-3-32-e g:conv-3-32-f h:concat-g-in i:conv-3-5-h" -P 16
SGE_Batch -r "e55-01-08" -c "python3 -u train.py e55-01-08 a:conv-3-32-in b:maxpool-1-100-a c:maxpool-100-1-a d:concat-a-b e:concat-c-d f:conv-3-32-e g:conv-3-32-f h:concat-g-in i:conv-3-5-h" -P 8
SGE_Batch -r "e55-01-16" -c "python3 -u train.py e55-01-16 a:conv-3-32-in b:maxpool-1-100-a c:maxpool-100-1-a d:concat-a-b e:concat-c-d f:conv-3-32-e g:conv-3-32-f h:concat-g-in i:conv-3-5-h" -P 16
