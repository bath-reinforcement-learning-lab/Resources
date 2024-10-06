# -1. What is this
You've gotten a fresh machine with a GPU on it and want to set it up. 

# 0. Get an OS
In this tutorial we'll be installing Linux on your machine. If your machine comes with pre-installed with Windows you might want to backup your activation key or create a dual boot. Consideration for dual boot: If you never intend to use Windows, you're just wasting a disk partition.

Feel free to pick your favorite Linux distribution, I recommend you pick something "popular" and "easy", which roughly translate to "I can find help online and there are ready packages for anything an average user needs" and "I don't want to spend hours configuring my system" (with few exceptions).

I personally recommend:
- Pop!_OS (this is based on Ubuntu but with less bloat and supposedly optimized support for devs e.g. comes with NVIDIA GPU support)
- Ubuntu
- TempleOS (for the brave)

To install a Linux distro (you can do this on your personal machine or the new machine, doesn't matter):
- Goto the website of the distribution. For example google: "Download ubuntu" and click the "ubuntu.com" result.
- Download the .iso file
- Burn the ISO image to a USB and make it bootable. This is possible via the terminal but I'd suggest just installing balenaEtcher or Rufus which are utilities that will do this for you without the need looking into stackoverflow when [dd](https://en.wikipedia.org/wiki/Dd_(Unix)) betrays you.
- Put the USB on your new machine and install Linux by pressing "Next" for a few minutes.
- Congrats, you now have a linux machine!

Lastly, some versions of Linux ship with **auto-suspend features**. This means that if you don't run a job for e.g. 30 minutes, you machine will suspend (not good, you  can't ssh to your machine anymore). Typically, you can tweak this in `Settings - Power/Power management - Suspend & Power Button - Automatic Suspend` (ish).

# 1. Enable SSH

Open a linux terminal and run the following.

```bash
$ sudo apt install openssh-server
$ sudo systemctl start ssh
$ sudo systemctl enable ssh
```

You should now be able to ssh into your machine with
```bash
ssh <usernameYouChoseWhenInstallingLinux>@<publicIpAddress>
# If your machine is department-provided
ssh <usernameYouChoseWhenInstallingLinux>@<bathUsername>.cs.bath.ac.uk
# For example mine is
ssh panayiotis@pp2024.cs.bath.ac.uk
# If you have errors with ssh try adding this flag to get more info
ssh -vvv panayiotis@pp2024.cs.bath.ac.uk
```


(Optional) If you want to ssh without a password (do this locally on the machine you ssh from)
```bash
# Create new SSH key exclusively for your machine
ssh-keygen -t rsa -b 4096 -C "pp2024@bath.ac.uk" -f ~/.ssh/labmachine_id_rsa
# Add key to OpenSSH auth agent
ssh-add -K ~/.ssh/labmachine_id_rsa  # only use the -K option if you are on macOS
# Copy public key to your machine
scp ~/.ssh/labmachine_id_rsa.pub panayiotis@pp2024.cs.bath.ac.uk:~/temp_id_rsa.pub
# SSH to your machine and add this public key to the authorized keys
ssh panayiotis@pp2024.cs.bath.ac.uk
mkdir .ssh
cat ~/temp_id_rsa.pub >> ~/.ssh/authorized_keys
rm ~/temp_id_rsa.pub
# Set proper permissions.
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
# Test it! (ssh from your personal machine to the remote one again)
exit # back to your machine
ssh panayiotis@pp2024.cs.bath.ac.uk
exit # back to your machine
# Add to .zshrc or .bashrc on your local machine
labmachine() {
    ssh-add -K ~/.ssh/labmachine_id_rsa
    ssh panayiotis@pp2024.cs.bath.ac.uk
}
# source .zshrc or .bashrc
source .zshrc
# Login from your local machine, replace all future ssh commands with this!
labmachine
```

# 2. (Optional) Install ZSH

```bash
sudo apt update
sudo apt install zsh -y
chsh -s $(which zsh)
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
# You need to logout and ssh back in for this to work
exit
ssh panayiotis@pp2024.cs.bath.ac.uk
```

Lastly, add `alias c="clear"` to your `~/.zshrc` (and then source it) so you can fidget on your terminal with `l` and `c`.

# 3. Essentials
The following command might install nothing, but it's just in case your linux distro left something essential (for your average needs as an ML researcher) behind

```bash
# Update and upgrade
sudo apt update && sudo apt upgrade -y
# Install essentials
sudo apt install build-essential dkms git curl wget unzip software-properties-common python3 python3-pip -y
```

