 #!/bin/bash
while read options; do echo $options; export options; run.sh; done <conditions.txt

