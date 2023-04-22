#!/bin/bash

# Function to swap two files
swap_files() {
  file1=$1
  file2=$2

  # Generate a random temporary file name
  temp_file="temp_$(uuidgen).tmp"

  # Rename file1 to the temporary file
  mv "$file1" "$temp_file"

  # Rename file2 to file1
  mv "$file2" "$file1"

  # Rename the temporary file to file2
  mv "$temp_file" "$file2"
}

# Define the paths to the .env and .env.test files
env_file=".env"
env_test_file=".env.test"

# Swap the files
swap_files "$env_file" "$env_test_file"

# Run pytest
pytest

# Swap the files back
swap_files "$env_file" "$env_test_file"
