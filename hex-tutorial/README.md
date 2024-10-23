# 0. Instructions
- Replace **pp2024** with your username in this tutorial & avoid skipping non-optional sections.
- I am using **pp2024-rl-dev-container** as the container name for everything here. Please use a different container name because otherwise, you will clash with my containers. Also, if you use more than one container, you'll need to add a suffix, e.g. pp2024-rl-dev-container-1, pp2024-rl-dev-container-2
- How to use this tutorial: fork it and keep your own template with your own package dependencies

# 1. Log into Hex

## 1.1 Easy way

```bash
# Pick one of the servers from https://hex.cs.bath.ac.uk/usage
# ssh <username>@<server_name>.cs.bath.ac.uk
ssh pp2024@garlick.cs.bath.ac.uk
```

## 1.2 Advanced way (optional, convenience)

Set up an SSH key for logging in and copying files without password verification.

```bash
# Create new SSH key exclusively for Hex
ssh-keygen -t rsa -b 4096 -C "pp2024@bath.ac.uk" -f ~/.ssh/hex_id_rsa
# Add key to OpenSSH auth agent
ssh-add -K ~/.ssh/hex_id_rsa  # only use the -K option if you are on macOS
# Copy key to Hex
scp ~/.ssh/hex_id_rsa.pub pp2024@garlick.cs.bath.ac.uk:~/temp_id_rsa.pub
# Login to Hex to add this public key to the authorized keys
ssh pp2024@garlick.cs.bath.ac.uk
mkdir .ssh
cat ~/temp_id_rsa.pub >> ~/.ssh/authorized_keys
rm ~/temp_id_rsa.pub
# Set proper permissions.
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
# Test it! (ssh from your machine to hex again)
exit # back to your machine
ssh pp2024@garlick.cs.bath.ac.uk
ssh -vvv pp2024@nitt.cs.bath.ac.uk 
# Add to .zshrc or .bashrc on your local machine
exit # back to your machine
hex() {
    local servername=$1
    ssh-add -K ~/.ssh/hex_id_rsa
    ssh pp2024@"$servername".cs.bath.ac.uk
}
# source .zshrc or .bashrc
source .zshrc
# Login from your local machine
hex garlick
```

# 2. TLDR Rules
- When choosing what GPU to use or what server to choose to connect to **PLEASE** check the [usage page of Hex](https://hex.cs.bath.ac.uk/usage). Here, I use *garlick* and some random GPUs from it for demonstration only
- Leave at least 1 GPU free
- Avoid MSc nodes during summer
- Home directory < 50 GB
- Watch memory & compute usage of your jobs (top, htop, nvidia-smi, hare usage)
- Release directories in /mnt/fast* when done
- GPU cloud storage isn't backed up. Backup your important files

  
# 3. Running jobs on Hex

In this tutorial, I've included a directory called `my-local-code-repo`. We will:
- Copy `my-local-code-repo` to Hex
- Build the docker image on Hex
- Create a queue of jobs using the code of `my-local-code-repo` and run them all inside a container on Hex.

## 3.1 Basic Hex setup + Copy your code on Hex
When on Hex, always work on one of the fast-mounted drives (scratch space), but delete your files when you're done if you're handling big (10 GB) amounts of data. These fast drives can be found on [https://hex.cs.bath.ac.uk/usage](https://hex.cs.bath.ac.uk/usage), e.g. `/mnt/fast0`, pick one with enough space. fast=SSD, faster=NVME.

```bash
# Once you ssh to Hex
cd /mnt/fast0
# Create a directory with your username (if it does not exist)
mkdir -p pp2024
hare reserve pp2024
# To reserve a random port (optional)
hare reserve !
# Check what you already reserved & what containers you are running
hare me
# Release space (will delete your files)
hare release /mnt/faster0/pp2024
rm -r /mnt/faster0/pp2024
# Extend expiration date by 3 months (auto-deletion on expiration)
hare extend -k 3m pp2024
hare help <command>
# To copy your code (my-local-code-repo) on Hex, run this on your local machine
rsync -uavz --progress my-local-code-repo pp2024@garlick.cs.bath.ac.uk:/mnt/fast0/pp2024
```

If you write code locally, you'll need to run `rsync -uavz --progress my-local-code-repo pp2024@garlick.cs.bath.ac.uk:/mnt/fast0/pp2024` whenever you want to run something on Hex (if you love over-engineering, create a script that runs whenever you save your editor that automatically runs the `rsync` command - can't include in this tutorial because it depends on the editor you're using). Alternatively, you can code directly on Hex (e.g. using [this extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-ssh)).

## 3.2 Run job using Hare
Hare is a wrapper on top of Docker used on Hex (adds a security layer). Hare also handles reserving storage and ports. I provide a `Dockerfile` and `requirements.txt` in `my-local-code-repo`. Both of these files should also be added to your code repository as they together handle the building of the Docker image. We are going to build it and run a container using hare. Everything from now on happens inside Hex, **not** on your local machine.

Hare syntax: `hare run <arguments> <image> <command and parameters>`


### How to build and run the container

```bash
# Build the docker file
hare build -t pp2024/rl-dev-image .
# Run your container. Your code lives in the /workspace directory inside the container.
hare run -it --rm -v $(pwd):/workspace --name pp2024-rl-dev-container --gpus '"device=1,5"' --user $(id -u):$(id -g) pp2024/rl-dev-image bash
# Explanation:
# -it interactive
# --rm remove after stopping
# -v $(pwd):/workspace mounts the current directory to the /workspace directory inside the container
# --gpus what GPUs to use
# --user you will be the same user inside the container (remove this to be root)
# Access a container that is currently running (rare usefulness)
hare exec -it pp2024-rl-dev-container bash
```

### How to install new packages

To install a new package to your image (you need to do this every time you need to install a new package)
```bash
# Run new container as root
hare run -it --rm -v $(pwd):/workspace --name pp2024-rl-dev-container --gpus '"device=0"' pp2024/rl-dev-image bash
cd workspace
pip install <package you want>
# To verify installation of a package (e.g. gymnasium)
python -c "import gymnasium; print(gymnasium.__version__)"
pip freeze > requirements.txt
exit # exit, stop and remove container
# Rebuild image
hare build --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g) -t pp2024/rl-dev-image .
# Delete dangling image (old image) - hare doesn't support this so this is wasted space (ignore)
# hare image prune
```

### How to schedule a queue of jobs + monitor them

Put all the commands you want to schedule in a file called `schedule.sh` inside your code repository `my-local-code-repo` (See example schedule file in this repo). Below is a breakdown of an example `schedule.sh` and what to modify in it (Ctrl+F "<CHANGE")

```bash
#!/bin/bash
# Log file location
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
LOGFILE="/workspace/progress_$TIMESTAMP.log"

# Start logging
echo "Starting schedule.sh execution at $(date)" > $LOGFILE

# Job 1
echo "Starting Command 1: ls -l" >> $LOGFILE
# <CHANGE THIS TO THE FIRST JOB>
python src/ppo.py --seed 10 --total_timesteps 100
echo "Completed Command 1" >> $LOGFILE

# Job 2
echo "Starting Command 2: pwd" >> $LOGFILE
# <CHANGE THIS TO THE SECOND JOB>
python src/ppo.py --seed 11 --total_timesteps 100
echo "Completed Command 2" >> $LOGFILE
```

Run the schedule (runs new container, runs all jobs inside, then stops and removes the container)
```bash
hare run -it --rm -v $(pwd):/workspace --name pp2024-rl-dev-container --gpus '"device=1,5"' --user $(id -u):$(id -g) pp2024/rl-dev-image /bin/bash schedule.sh
```

Check progress & monitor
```bash
# Check the exact name of the log file
# REPLACE * with the exact timestamp
cat my-local-code-repo/progress_*.log
# Automatic ordering and catting the latest one - avoid
cat $(ls -ltr progress_*.log | tail -n 1 | awk '{print $NF}')
# Monitor GPU usage + memory utilization
nvidia-smi
# See your container
hare pso | grep pp2024
# Memory and CPU usage of container
hare stats pp2024-rl-dev-container
hare usage
# Check processes running on your behalf
ps -aux | grep pp2024
# Use top outside the container
top
# Use top inside the container
hare top pp2024-rl-dev-container
# Check any logs (e.g. if you print to stdout)
hare logs pp2024-rl-dev-container
# Checking logs when you know there are too many
hare logs -f -n 16 pp2024-rl-dev-container
```

### Cleanup after yourself

When a container is stopped, it's automatically removed because we pass the `--rm` flag. But we need to make sure it's stopped.

```bash
# When in doubt, run this to see how many of your containers are currently running
hare me
# To stop it from running (will be auto-removed)
hare stop pp2024-rl-dev-container
# When something goes wrong, you can try
hare rm pp2024-rl-dev-container
hare kill pp2024-rl-dev-container
```

### Copy data back to your personal machine

This is useful if you want to check any plots (this might also be possible with port forwarding).

```bash
# Copy all files back to your personal machine (run this on your machine)
rsync -uavz --progress pp2024@garlick.cs.bath.ac.uk:/mnt/fast0/pp2024/my-local-code-repo /path/to/local-destination
# Ideally, don't copy everything just copy the results of one particular run
rsync -uavz --progress pp2024@garlick.cs.bath.ac.uk:/mnt/fast0/pp2024/my-local-code-repo/runs/CartPole-v1__ppo__10__1717239825 /path/to/local-destination
```


# 4. Everyday routine

```bash
# 1. Copy code to Hex
rsync -uavz --progress my-local-code-repo pp2024@garlick.cs.bath.ac.uk:/mnt/fast0/pp2024
# 2. Run schedule
hare run -it --rm -v $(pwd):/workspace --name pp2024-rl-dev-container --gpus '"device=1,5"' --user $(id -u):$(id -g) pp2024/rl-dev-image /bin/bash schedule.sh
# 3. Check usage (check respective section)
# 4. Cleanup after yourself (check respective section)
# 5. Copy files back to your personal machine (run this on your machine)
rsync -uavz --progress pp2024@garlick.cs.bath.ac.uk:/mnt/fast0/pp2024/results-folder /path/to/local-destination
# When in doubt
hare me
```


# 5. Closing thoughts

Make your life easier and put the following lines on the bottom of `/homes/pp2024/.bashrc` on Hex (login and logout after you do this or `source .bashrc`)

```
# Bind up and down arrow keys to history search
bind '"\e[A": history-search-backward'
bind '"\e[B": history-search-forward'

# Enable tab completion to cycle through suggestions
bind 'TAB:menu-complete'
```

Lastly, when an ssh connection locks you can kill it by pressing: `Enter`, `~`, `.`

Written with ❤️ by @panispani
