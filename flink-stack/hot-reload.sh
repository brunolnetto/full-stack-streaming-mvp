#!/bin/sh

# Requirements: inotify-tools, curl
# Usage: ./hotreload.sh

JOBMANAGER_URL="http://jobmanager:8081"
SRC_DIR="/opt/src"

submit_job() {
  local jobfile="$1"
  echo "Submitting job: $jobfile"
  
  # Create a simple Python script that can be executed
  python3 "$jobfile"
  
  echo "Job $jobfile executed successfully!"
}

# Initial submit for all job files
for job in $SRC_DIR/*_job.py; do
  [ -e "$job" ] && submit_job "$job"
done

# Watch for changes and resubmit
inotifywait -m -e close_write $SRC_DIR |
while read -r directory events filename; do
  if echo "$filename" | grep -q '_job.py$'; then
    echo "Detected change in $filename. Resubmitting job."
    submit_job "$directory$filename"
  fi
done 