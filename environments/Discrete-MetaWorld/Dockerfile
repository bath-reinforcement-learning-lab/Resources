FROM pytorch/pytorch:1.12.1-cuda11.3-cudnn8-runtime
# if you want tf then use tensorflow/tensorflow

# need to have the tag -y or -yes on everything otherwise it will abort

RUN apt update
RUN apt install -y libosmesa6-dev libgl1-mesa-glx libglfw3
RUN apt install -y python3-pip
RUN apt install -y patchelf
RUN pip install numpy


RUN apt-get update -y -q \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    curl \
    git \
    libgl1-mesa-dev \
    libgl1-mesa-glx \
    libglew-dev \
    libosmesa6-dev \
    software-properties-common \
    net-tools \
    vim \
    virtualenv \
    wget \
    xpra \
    xserver-xorg-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
	
RUN DEBIAN_FRONTEND=noninteractive add-apt-repository --yes ppa:deadsnakes/ppa && apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install --yes python3.6-dev python3.6 python3-pip

# need to download and move the .mujoco file into the working dir (I think actually root.)

RUN pip3 install -U 'mujoco-py<2.2,>=2.1'
RUN pip install mujoco-py
RUN pip install scipy

ENV LD_LIBRARY_PATH $LD_LIBRARY_PATH:/root/.mujoco/mujoco210/bin
# add the following to the bash script: LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/root/.mujoco/mujoco210/bin

# ALL ABOVE will get MUJOCO working on HEX with cuda

RUN apt install -y git
RUN pip install git+https://github.com/rlworkgroup/metaworld.git@master#egg=metaworld

# Before this will work you need to move the .mujoco file to root.
# This is now ready to run metaworld on cuda on hex.