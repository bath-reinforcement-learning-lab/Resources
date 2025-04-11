# -1. What is this
You've got a fresh machine with a GPU on it (possibly from the University Department) and want to set it up. In this tutorial, please replace **pp2024** with your username and avoid skipping non-optional sections.

# 0. Get an OS
In this tutorial, we'll install Linux on your machine. If your machine comes pre-installed with Windows, you might want to back up your activation key or create a dual boot. Consideration for dual boot: If you never intend to use Windows, you're just wasting a disk partition.

Feel free to pick your favourite Linux distribution. I recommend you choose something "popular" and "easy", which roughly translates to "I can find help online with little effort, and there are ready packages for anything an average user needs" and "I don't want to spend hours configuring my system" (with few exceptions).

I personally recommend:
- Pop!_OS (this is based on Ubuntu but with less bloat and supposedly optimized support for devs e.g. comes with NVIDIA GPU support)
- Ubuntu
- TempleOS (for the brave)

To install a Linux distro (you can do this on your personal machine or the new machine, doesn't matter):
- Go to the distribution's website. For example, google: "Download ubuntu" and click the "ubuntu.com" result.
- Download the .iso file
- Burn the ISO image to a USB and make it bootable. This is possible via the terminal, but I'd suggest just installing *balenaEtcher* or *Rufus*, which are utilities that will do this for you without the need to look into Stack Overflow when [dd](https://en.wikipedia.org/wiki/Dd_(Unix)) betrays you.
- Plug the USB into your new machine, turn it on, and install Linux by pressing "Next" for a few minutes.
- Congrats, you now have a Linux machine!

Lastly, some versions of Linux ship with **auto-suspend features**. This means that if you don't run a job for, e.g. 30 minutes, your machine will suspend (not good, you can't SSH to your machine anymore). Typically, you can tweak this in `Settings - Power/Power management - Suspend & Power Button - Automatic Suspend` (ish).

# 1. Enable SSH

Open a terminal on your new Linux machine and run the following.

```bash
$ sudo apt install openssh-server
$ sudo systemctl start ssh
$ sudo systemctl enable ssh
```

To SSH into a university-managed device you need to either be connected to the university network (eduroam) or use the university's VPN (check instructions on how to set this up on your personal device [here](https://www.bath.ac.uk/guides/setting-up-vpn-on-your-device/)).
You should now be able to ssh into your new machine (e.g. from your laptop) with
```bash
ssh <usernameYouChoseWhenInstallingLinux>@<publicIpAddress>
# If your machine is department-provided, this looks like this
ssh <usernameYouChoseWhenInstallingLinux>@<bathUsername>.cs.bath.ac.uk
# For example, mine is
ssh panayiotis@pp2024.cs.bath.ac.uk
# If you have errors with ssh try adding this flag to get more info
ssh -vvv panayiotis@pp2024.cs.bath.ac.uk
```


(Optional) If you want to ssh without a password, do the following locally on the machine you want to ssh from
```bash
# Create a new SSH key exclusively for logging into your new machine 
ssh-keygen -t rsa -b 4096 -C "pp2024@bath.ac.uk" -f ~/.ssh/labmachine_id_rsa
# Add key to OpenSSH auth agent
ssh-add -K ~/.ssh/labmachine_id_rsa  # only use the -K option if you are on macOS
# Copy the new public key to your new machine
scp ~/.ssh/labmachine_id_rsa.pub panayiotis@pp2024.cs.bath.ac.uk:~/temp_id_rsa.pub
# SSH to your new machine and add the public key to the authorized keys
ssh panayiotis@pp2024.cs.bath.ac.uk
mkdir .ssh
cat ~/temp_id_rsa.pub >> ~/.ssh/authorized_keys
rm ~/temp_id_rsa.pub
# Set proper permissions to the authorized keys.
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
# Test it! (ssh from your personal machine to the remote one again and you shouldn't be prompted for a password)
exit # back to your personal machine
ssh panayiotis@pp2024.cs.bath.ac.uk
exit # back to your personal machine
# Add this to .zshrc or .bashrc on your local machine
labmachine() {
    ssh-add -K ~/.ssh/labmachine_id_rsa
    ssh panayiotis@pp2024.cs.bath.ac.uk
}
# source .zshrc or .bashrc
source .zshrc
# Login from your local machine
labmachine
```
All following sections are to be performed on your new machine (SSH into it), unless otherwise specified. 

# 2. (Optional) Install ZSH

```bash
sudo apt update
sudo apt install zsh -y
chsh -s $(which zsh)
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
# You need to logout and ssh back in for this to work
exit
ssh panayiotis@pp2024.cs.bath.ac.uk # or "labmachine"
```

(Optional) Lastly, add `alias c="clear"` to your `~/.zshrc` (and then source it) so you can fidget on your terminal with `l` and `c`.
```bash
nano ~/.zshrc
# Add on the last line (without a # at the start):
# alias c="clear"
# then exit nano
source ~/.zshrc
# yes these are actual commands:
c
l
c
```

# 3. Essentials
The following command might install nothing, but it's just in case your chosen Linux distro left something essential (for your average needs as an ML researcher) behind

```bash
# Update and upgrade
sudo apt update && sudo apt upgrade -y
# Install essentials
sudo apt install build-essential dkms git curl wget unzip software-properties-common python3 python3-pip htop -y
```

(Optional) Install vim
```bash
sudo apt install -y vim
```

# 4. Install NVIDIA Drivers, CUDA Toolkit, and cuDNN

## Check if you have NVIDIA drivers
```bash
# If this returns something, look in the middle of the first line. If it says something like "Driver Version: 550.67", you're good. If you have installed PopOS, this is what you should expect.
$ nvidia-smi
```

If you are on Ubuntu and want to install NVIDIA drivers, follow this tutorial [https://ubuntu.com/server/docs/nvidia-drivers-installation](https://ubuntu.com/server/docs/nvidia-drivers-installation). If you are on TempleOS, you are the NVIDIA driver.

**Common NVIDIA driver issue** (mismatch between drivers and NVIDIA management library NVML). If you get an error similar to the following:
```
Failed to initialize NVML: Driver/library version mismatch
NVML library version: 560.35
```
Try rebooting your machine (your ssh connection will die, if you have full disk encryption, you might need physical access to the machine to finish booting)
```
sudo reboot
```


## Install CUDA toolkit

The CUDA drivers enable your OS and hardware to communicate with the NVIDIA GPU. The CUDA toolkit provides you with the development environment to do so (what people use to write/compile/run code and interact with the GPU at a high level). For example, the env environment has libraries (cuDNN, cuBLAS, optimized libraries for the GPU) and a compiler to write and run code using the GPU (if you write CUDA C/C++, the compiler will translate it for your NVIDIA GPU). You need this if you want to use PyTorch or TensorFlow with GPU acceleration.

Go to [https://developer.nvidia.com/cuda-downloads](https://developer.nvidia.com/cuda-downloads) and select the following options:
- Operating System: Linux
- Architecture: x86_64 (depends on you)
- Distribution: Ubuntu (depends on you)
- Version: 22.04 (depends on you, POP!_OS is Ubuntu)
- Installer Type: runfile (local)

The website will provide you with installation instructions, execute them on your new machine:

```bash
# For example, please don't download this one, it might be outdated when you're reading this
wget https://developer.download.nvidia.com/compute/cuda/12.6.2/local_installers/cuda_12.6.2_560.35.03_linux.run
# Execute (Don't abort if prompted, accept EULA license agreement, de-select reinstallation of nvidia drivers)
sudo sh cuda_12.6.2_560.35.03_linux.run
# If you want to reinstall CUDA drivers, remove the old ones by
sudo apt-get purge 'nvidia-*'
sudo reboot
# If you need to uninstall the toolkit for whatever reason
# Run cuda-uninstaller in /usr/local/cuda-12.6/bin
```

Then add the following to the end of your `~/.zshrc` (open it with nano or vi/vim). Find the right CUDA path, it's usually `/usr/local/cuda-X.X` (this should be in the output of the previous command)
```bash
export PATH=/usr/local/cuda-12.6/bin${PATH:+:${PATH}}
export LD_LIBRARY_PATH=/usr/local/cuda-12.6/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
```

Finally, verify this worked with
```bash
nvcc --version
```

Note that you still need to install cuDNN separately (it's not bundled with the toolkit for reasons, but you need the toolkit to use cuDNN). Go to [https://developer.nvidia.com/cudnn-downloads](https://developer.nvidia.com/cudnn-downloads) and select the cuDNN compatible with your CUDA version, similarly to the CUDA toolkit (e.g., for this tutorial, my CUDA is 12.6).
```bash
# For me, please follow the instructions the nvidia website gives you for your setup, the first command downloads cuDNN, all of these should be executed on your new machine
wget https://developer.download.nvidia.com/compute/cudnn/9.5.0/local_installers/cudnn-local-repo-ubuntu2204-9.5.0_1.0-1_amd64.deb
sudo dpkg -i cudnn-local-repo-ubuntu2204-9.5.0_1.0-1_amd64.deb
# The following command should be last line of output from the previous one
sudo cp /var/cudnn-local-repo-ubuntu2204-9.5.0/cudnn-*-keyring.gpg /usr/share/keyrings/
sudo apt-get update
sudo apt-get -y install cudnn-cuda-12
```

# 5. Install Docker and NVIDIA container toolkit

Docker is for running containers. The NVIDIA Container Toolkit allows code inside your containers to use GPUs. While you can probably skip this, I highly recommend running your code inside containers. It will make your research and papers more reproducible. While containers can get complicated in general, as a researcher, your setup should be fairly standard and simple.

You can definitely run jobs outside of Docker much more easily. The main reason for using Docker is that it allows for reproducibility (both on your side and for others running your code). Also, if you follow the instructions here, it really shouldn't be that hard (small sacrifice for a big payoff; you might even like containers by the end of your PhD!).

## Install docker engine
```bash
# Setup
sudo apt update
sudo apt install ca-certificates curl gnupg lsb-release -y

sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Add docker repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Finally install docker engine
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y

# Verify installation
sudo docker run hello-world

# Allow your non-root user to manage docker
sudo groupadd docker
sudo usermod -aG docker $USER
# Logout and login for group changes to take effect
exit
labmachine # or ssh
# Verify that your non-root user can run docker machines without using sudo
docker run hello-world
```

## Install NVIDIA Container Toolkit

Nvidia setup from their docs: [https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html). The below setup is similar.

```bash
# Setup the package repository
distribution=ubuntu22.04

curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | \
sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg

curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | \
sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
sudo tee /etc/apt/sources.list.d/nvidia-docker.list

# Install NVIDIA container toolkit
sudo apt update
sudo apt install -y nvidia-docker2
sudo systemctl restart docker

# Verify installation
# You should be able to see "nvidia-smi" output from within the docker container (you can compare it with the "nvidia-smi" output from outside the docker container)
nvidia-smi
# This command changes based on your CUDA version (here, 12.6.2) and Ubuntu version (here 22.04). Please check: https://hub.docker.com/r/nvidia/cuda and choose <cuda-version>-runtime-ubuntu<version> as your docker tag. Mine is 12.6.2-runtime-ubuntu22.04
docker run --rm --gpus all nvidia/cuda:12.6.2-runtime-ubuntu22.04 nvidia-smi
```

# 6. Install Python & virtual envs

## Install Python
Python should be installed by default. If it's not:
```bash
# Check if Python is installed
python3 --version
# If Python is installed, skip to the following section about miniconda
# Update package lists (to have the latest versions of packages)
sudo apt update
sudo apt install python3
# Pip should come with python3, but to be sure do
sudo apt install python3-pip
# Set python3 to be the default when typing python (check if python starts python2 or python3 by just running "python" and reading the first line)
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3 1
```
## Install miniconda

I personally prefer `conda` to `venv`/`virtualenv`/`pyenv`/`poetry`/etc. This is a very subjective choice. If you feel more comfortable with a different way to create and manage virtual environments, please use that one instead.

```bash
# Downlaod and install miniconda
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
source ~/.zshrc
# Create a conda env called 'ml'
conda create -n ml python=3.10 -y
# This is all you usually need to do to load your dev env. You can add this to the end of your .zshrc, and it will be autorun every time you start a new shell via ssh ;)
conda activate ml
```

# 7. (Optional) Local installation of PyTorch

If, for some reason, you want to have a local installation of PyTorch. If you usually use Docker, you'll be running your code inside containers that have PyTorch installed already. This step isn't really required, including for completeness. Go to [https://pytorch.org/get-started/locally/](https://pytorch.org/get-started/locally/) and get the latest command

```bash
# Replace this with the command you get from the pytorch website
conda install pytorch torchvision torchaudio pytorch-cuda=12.6 -c pytorch -c nvidia -y
# Verify installation
python -c "import torch; print(torch.__version__); print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0))"
```

# 8. Handling Code

## Cloning code from GitHub/GitLab

To clone GitHub/GitLab code directly in your new machine, you'll need to create an SSH key in it and add it to your GitHub/GitLab account (if you intend to code locally, you need to do this locally, but you've probably already done it). For example this is how you do it on GitHub: [https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account)


## Code remotely or copy code regularly

You can code directly on your new machine via ssh on your laptop. Remote development like this is easy to set up in VSCode (see this [short tutorial](https://code.visualstudio.com/docs/remote/ssh)). As long as you don't have internet issues and you don't mind not having offline access to your code, this is probably the best (and simplest) option.

Alternatively, you can code locally and copy the code to your GPU machine only when you need to run some experiments. This is good if you expect to have frequent internet issues. You can copy your code from your local machine to your GPU machine with:
```bash
# I excluded 'results' and 'logs' directories. Adjust this accordingly, it copies the files of the current directory and all subdirectories into 'my-amazing-project'
rsync -uavz --exclude='results/' --exclude='logs/' . panayiotis@pp2024.cs.bath.ac.uk:/home/panayiotis/my-amazing-project/
```
Note: you can also set up a VSCode script that runs `rsync` every time you save or create a new command shortcut for it (like we did with 'labmachine').
```bash
# Add to .zshrc. Note that you'll need to change 'my-amazing-project' every time you want to copy to a new project or have multiple sync commands. Use this with caution, as you can accidentally overwrite one project with another! (hence, the name of the command includes as a suffix the name of the project)
alias syncamazingproject="rsync -uavz --exclude='results/' --exclude='logs/' . panayiotis@pp2024.cs.bath.ac.uk:/home/panayiotis/my-amazing-project/"
```

# 9. Example usage: scheduling and running jobs

## Setting up a schedule of jobs

There are better ways to schedule jobs than what I'll show here. However, with 1 non-shared GPU, you pretty much have to run jobs sequentially, and no one will kill your processes (so what I show here is probably enough).

I include a folder called `my-local-code-repo`. It includes a PPO implementation. In this section I will schedule 2 runs of that PPO implementation with different arguments, all run inside a Docker container, and using the GPU. Note for the observant: we just verify that the PPO implementations have access to the GPU rather than stress testing it (if you don't get this comment, ignore). 

Put all the commands you want to schedule in a `schedule.sh` file inside your code repository `my-local-code-repo` (See example schedule file in this repo). Below is a breakdown of an example `schedule.sh` and what to modify in it (Ctrl+F "<CHANGE")

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

## Build and run the container


If you have a different CUDA version than mine, building the docker container in the `my-local-code-repo` might break because of package version clashes/incompatibility (the build command is the first command of next code snippet). **Only** in that case, do the following
```bash
rm requirements.txt
touch requirements.txt
# Build
docker build -t pp2024/ppo-image .
# Run
docker run -it --rm -v $(pwd):/workspace --name pp2024-ppo-container --gpus all pp2024/ppo-image bash
# Let pip determine what package versions work with you
pip install absl-py cloudpickle docstring_parser etils eval_type_backport Farama-Notifications filelock fsspec glfw grpcio gymnasium imageio importlib_metadata importlib_resources Jinja2 Markdown markdown-it-py MarkupSafe mdurl mpmath mujoco networkx numpy pillow protobuf Pygments PyOpenGL rich shtab six sympy tensorboard tensorboard-data-server torch torchaudio torchvision tqdm triton typing_extensions tyro Werkzeug zipp
# Save your package versions
pip freeze > requirements.txt
# Rebuild with the right package versions
docker build -t pp2024/ppo-image .
# Prune old docker image
docker image prune
```

Regardless of whether you executed the previous code block or not, let's check that you can run the container and have GPU access inside.
```bash
# Make sure you are in the directory with the Dockerfile
# Build the docker image
docker build -t pp2024/ppo-image .
# Run the container. The current code directory lives in the /workspace directory inside the container.
# Explanation:
# -it interactive
# --rm remove after stopping
# -v $(pwd):/workspace mounts the current directory to the /workspace directory inside the container
# --gpus what GPUs to use
# --user you will be the same user inside the container (remove this to be root)
docker run -it --rm -v $(pwd):/workspace --name pp2024-ppo-container --gpus all pp2024/ppo-image bash
# Alternative to use only a specific GPU
# '"device=0"'
# You can also specify multiple GPUs with
# '"device=0,2,5"'
docker run -it --rm -v $(pwd):/workspace --name pp2024-ppo-container --gpus '"device=0"' pp2024/ppo-image bash
# Now you are inside the container
nvidia-smi # should display the exact GPUs you pass as arguments
python check_installation.py
# From another terminal, you can check that the container is running with
docker ps
# Exit the container (run inside the container)
exit
```

Now run a container and run your `schedule.sh` inside it (what you will usually do):
```bash
# No need to re-build the container with
# docker build -t pp2024/ppo-image .
# Note that we run the container with -d, detached mode, so that the container isn't tied to our terminal session. If you close the SSH connection, this will keep on running.
docker run -d --rm -v $(pwd):/workspace --name pp2024-ppo-container --gpus all pp2024/ppo-image /bin/bash schedule.sh
```

## Install new packages

Every time you need to install a new package
```bash
# Run new container as root
docker run -it --rm -v $(pwd):/workspace --name pp2024-ppo-container --gpus all pp2024/ppo-image bash
pip install <package you want>
# To verify installation of a package (e.g. gymnasium)
python -c "import gymnasium; print(gymnasium.__version__)"
pip freeze > requirements.txt
exit # exit, stop and remove container
# Rebuild image
docker build -t pp2024/ppo-image .
# Delete dangling image (old image is useless because you rebuilt it)
docker image prune
```

## Monitor your jobs

```bash
# Check the exact name of the log file
# REPLACE * with the exact timestamp
cat my-local-code-repo/progress_*.log
# Automatic ordering and catting the latest one - avoid
cat $(ls -ltr progress_*.log | tail -n 1 | awk '{print $NF}')
# Monitor GPU usage + memory utilization
nvidia-smi
# See your container
docker ps | grep pp2024
# Memory and CPU usage of container
docker stats pp2024-ppo-container
# Use top outside the container
top
htop
# Monitor current running containers
watch -n1 docker ps
# Monitor GPU usage
watch -n 1 nvidia-smi
# Run this outside the container, it will run top inside the container and give you the output
docker top pp2024-ppo-container
# Check any logs (e.g. if you print to stdout)
docker logs pp2024-ppo-container
# Checking logs when you know there are too many
docker logs -f -n 16 pp2024-ppo-container
# Access the running container to check what is going on inside (rare usefulness)
docker exec -it pp2024-ppo-container bash
```

## Cleanup after yourself

When a container is stopped, it's automatically removed because we pass the `--rm` flag. But we need to make sure it's stopped.

```bash
# List all containers that are currently running
docker ps
# To stop it from running (will be auto-removed in this case because of --rm)
docker stop pp2024-ppo-container
# When something goes wrong, you can try
docker rm pp2024-ppo-container
docker kill pp2024-ppo-container
```

## Copy data back to your personal machine

This is useful if you want to check any plots (this might also be possible with port forwarding).

```bash
# Ideally, don't copy everything just copy the results of one particular run
rsync -uavz --progress panayiotis@pp2024.cs.bath.ac.uk:/home/panayiotis/my-local-code-repo/runs/CartPole-v1__ppo__10__1717239825 /path/to/local-destination
# Copy all files back to your personal machine (run this on your machine)
# Avoid to prevent overwriting your codebase by mistake!
rsync -uavz --progress panayiotis@pp2024.cs.bath.ac.uk:/home/panayiotis/my-local-code-repo /path/to/local-destination
```

# 10. Everyday routine

```bash
# 1. Copy code to Hex (not needed if already copied there)
# Either code remotely via SSH or copy the code every time you make a change.
rsync -uavz --progress my-local-code-repo panayiotis@pp2024.cs.bath.ac.uk:/home/panayiotis/
# 2. Run a schedule of jobs
docker run -it --rm -v $(pwd):/workspace --name pp2024-ppo-container --gpus all pp2024/ppo-image /bin/bash schedule.sh
# 3. Check usage (check respective section)
# 4. Cleanup after yourself (check respective section)
# 5. Copy files back to your personal machine (run this on your machine)
rsync -uavz --progress panayiotis@pp2024.cs.bath.ac.uk:/home/panayiotis/results-folder /path/to/local-destination
```

Written with ❤️ by @panispani
