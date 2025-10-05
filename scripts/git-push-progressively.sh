#!/bin/bash

SCRIPTS_DIR=$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}" || echo "${BASH_SOURCE[0]}")")" && pwd)/
source ${SCRIPTS_DIR}utils.sh

# Check if the commit message is passed as an argument
if [ $# -eq 0 ]; then
    log "ERROR: please provide a commit message as an argument." >&2
    exit 1
fi

commit_message=$1

while true; do
    # Get a list of modified files
    IFS=$'\n'
    files=($(git status --porcelain | awk 'BEGIN{srand()} {print rand() "\t" $0}' | sort -n | cut -f2-))

    # Check if the file list is empty
    if [ ${#files[@]} -eq 0 ]; then
        log "No files to add. Ending script."
        break
    fi

    # Add the files to the git index
    for file in "${files[@]}"; do
        status=$(echo "$file" | awk '{print $1}')
        file_path=$(echo "$file" | awk '{print substr($0, index($0,$2))}')
        file_path=${file_path%\"}
        file_path=${file_path#\"}
        if [ -n "$file_path" ]; then
            if [ "$status" == "D" ]; then
                if git ls-files --error-unmatch "$file_path" >/dev/null 2>&1; then
                    git rm --cached "$file_path"
                fi
            elif [ "$status" == "??" ]; then
                git add "$file_path"
            else
                git add "$file_path"
            fi
            # Commit and push
            git commit -m "$commit_message"
            git push
        fi
    done
done