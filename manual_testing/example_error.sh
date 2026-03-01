#!/bin/sh

echo "this is stdout text"

>&2 echo "this is stderr text"

exit 1
