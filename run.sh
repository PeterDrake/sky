#!/bin/bash

echo $options
# The %% * is a perverse trick to get first word of options, which is the job name
#SGE_Batch -r "${options%% *}" -c "python3 -u preprocess.py $options" -P 1

SGE_Batch -r "e54-00-01" -c "python3 -u train.py e54-00-01 a:conv-3-32-in b:maxpool-1-100-a c:maxpool-100-1-a d:concat-a-b e:concat-c-d f:conv-3-32-e g:conv-3-32-f h:concat-g-in i:conv-3-5-h" -P 1
SGE_Batch -r "e54-00-32" -c "python3 -u train.py e54-00-32 a:conv-3-32-in b:maxpool-1-100-a c:maxpool-100-1-a d:concat-a-b e:concat-c-d f:conv-3-32-e g:conv-3-32-f h:concat-g-in i:conv-3-5-h" -P 1
SGE_Batch -r "e54-01-01" -c "python3 -u train.py e54-01-01 a:conv-3-32-in b:maxpool-1-100-a c:maxpool-100-1-a d:concat-a-b e:concat-c-d f:conv-3-32-e g:conv-3-32-f h:concat-g-in i:conv-3-5-h" -P 32
SGE_Batch -r "e54-01-32" -c "python3 -u train.py e54-01-32 a:conv-3-32-in b:maxpool-1-100-a c:maxpool-100-1-a d:concat-a-b e:concat-c-d f:conv-3-32-e g:conv-3-32-f h:concat-g-in i:conv-3-5-h" -P 32
