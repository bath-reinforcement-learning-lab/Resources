#!/bin/bash
# Log file location
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
LOGFILE="/workspace/progress_$TIMESTAMP.log"

# Start logging
echo "Starting schedule.sh execution at $(date)" > $LOGFILE

# Job 1
echo "Starting Command 1: ls -l" >> $LOGFILE
python src/ppo.py --seed 10 --total_timesteps 100
echo "Completed Command 1" >> $LOGFILE

# Job 2
echo "Starting Command 2: pwd" >> $LOGFILE
python src/ppo.py --seed 11 --total_timesteps 10000
echo "Completed Command 2" >> $LOGFILE

# Job 3
echo "Starting Command 3: pwd" >> $LOGFILE
python src/ppo.py --seed 13 --total_timesteps 100
echo "Completed Command 3" >> $LOGFILE