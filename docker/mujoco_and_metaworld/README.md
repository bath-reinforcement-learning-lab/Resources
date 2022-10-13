
# Mujoco and Metaworld

I’ve included just a single Dockerfile here. It will work for both Mujoco and Metaworld. 

Unfortunately, it’s not quite as simple as just building the image. There are some file dependencies which you will have to download and then point to for environmental variables. Lets take it step by step.

1. Go here and download the mujoco files (do this on your local machine) [https://mujoco.org/download/mujoco210-linux-x86_64.tar.gz](https://mujoco.org/download/mujoco210-linux-x86_64.tar.gz)
2. Extract them and move them to your Hex area. I use:
    
    ```bash
    rsync -uav .mujoco tc2034@aching.cs.bath.ac.uk
    ```
    
3. Download the Dockerfile here and also move them to your hex area
4. Log into Hex and build the image:
    
    ```bash
    hare build -t <my username>/<my image name>
    ```
    
5. Start the container as we have done in the tutorial:
    
    ```bash
    hare run -it --gpus device=0  -v "$(pwd)":/app <my username>/<my image name> bash
    ```
    
6. Now your .mujoco folder will be in /app you need to move this to /root (if you can’t see it with “ls” it’s because it is a hidden folder. It is there don’t worry!
    
    ```bash
    cd ..
    mv /app/.mujoco /root
    ```
    
7. Next copy and paste this:
    
    ```bash
    LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/root/.mujoco/mujoco210/bin
    ```
    
8. Now just exit the image and commit it as the same name you built it with.
    
    ```bash
    exit
    hare me #find the name of your container
    hare commit <container name> <my username>/<my image name>
    hare rm <container name>
    ```
    
9. You are now all ready to use Mujoco and Metaworld with Hex GPU support. Just run the container up again and you can run your code as usual.
    
    ```bash
    hare run <my username>/<my image name>
    ```
    
10. Any issues just contact me (Tom C)
