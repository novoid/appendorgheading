#!/bin/sh

output="output1.org"

# initialize the output file with a nice heading:
echo "* This is the main heading   :tag1:" > "${output}"

../../appendorgheading/__init__.py \
  --output ${output} \
  --level 2 \
  --keyword MYTODO \
  --priority C \
  --title "This is my heading title" \
  --tags "tag2 tag_3" \
  --scheduled "<2019-12-29 Sun 11:59>" \
  --deadline "<2019-12-30 Mon 09:38>" \
  --properties "CREATED:<2019-12-31 Tue 14:02>;demo:yes; example: yes ; curious: for sure" \
  --section "This is used as the section text or body of the heading.\nThis is a second line of it." \
  --filecontent input1.log \
  --blocktype EXAMPLE \
  --nosanitize

 # end


