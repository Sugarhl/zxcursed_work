#!/bin/bash

# Define default result file name
result_file="project.txt"

# Define default behavior for result file deletion
delete_file=false

# Parse command line options
while getopts "f:d" opt; do
  case $opt in
    f)
      result_file=$OPTARG
      ;;
    d)
      delete_file=true
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
    :)
      echo "Option -$OPTARG requires an argument." >&2
      exit 1
      ;;
  esac
done

# Remove options from the argument list
shift $((OPTIND -1))

# Delete the result file if the -d option was used
if $delete_file && [ -e "$result_file" ]; then
  rm "$result_file"
fi

# Find files and process each one
find "$1" -type f -print0 | while read -d $'\0' file
do
    file_type=$(file -b --mime-type "$file")
    if [[ $file_type == *"text"* ]]; then
        echo "Router $(sed "s|${HOME}/zxcursed_work/server/||" <<< $file):" >> "$result_file"
        # sed -e 's/^/  /' "$file" >> "$result_file"
        echo "" >> "$result_file"
    fi
done
