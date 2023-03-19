#!/bin/bash
files=$(ls -p "$1" | grep -v / )

if [[ -z $1 ]]; then
  echo "Nothing to find"
elif [[ ! -z "${files}" ]]; then
  echo "There are $(echo "${files}" | wc -l) files in $(pwd)/$1"
else 
  echo "Directory not found"
fi