#!/bin/sh

output="output1.org"

# initialize the output file with a nice heading:
echo "* This is the main heading   :tag1:" > "${output}"

../../appendorgheading/__init__.py --nodaily

 # end


