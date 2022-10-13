I imagine everyone should be using the GPU's on hex and therefore everyone will have there own Dockerfile for each of their resources. It makes sense that we share these resources.

In this resource there will be a tutorial on how to set up Dockerfiles / images / containers in order to use HEX. 
(I will do this shortly)

Then there should be extra sensibly named pages which contain a Dockerfile for each resource we might try to use. For instance one which allows GPU use on Hex with Mujoco or Meta-world.


# Docker Tutorial

Docker consists of three parts: A Dockerfile, an Image and a Container. 

In short. An image is similar to a virtual environment, but is more powerful; essentially it is a completely standalone virtual computer which runs on the same hardware. A container is just the place where the image is being run. A Dockerfile is just a method to build an image with the exact dependencies required. 

**This is a practical tutorial.** If you wish to learn more about Docker on Hex then refer to Tom Haines tutorials on the Hex the help pages: [https://hex.cs.bath.ac.uk/wiki/gollum/overview/docker/](https://hex.cs.bath.ac.uk/wiki/gollum/overview/docker/)

You *NEED* to use Docker to use GPU’s on Hex. I found that it took me a day or so to understand and build a Dockerfile which allowed me to run Mujoco and Metaworld. Therefore I hope that this tutorial will accelerate anybody else who is struggling. 

For ease of understanding, this tutorial will assume that you will always want to build you own custom image. It is easy and will enable you complete flexibility. 

1. Decide if you will use TensorFlow or Pytorch, then your *base* image will be either:
    1. tensorflow/tensorflow:latest-gpu
    2. pytorch/pytorch:1.12.1-cuda11.3-cudnn8-runtime (this is what I use there are other examples)
2. ssh onto a terminal on Hex, and on your local machine open a notepad file and save it as Dockerfile (exactly like this, no extension). We will use this notepad file to build the Dockerfile as we build the image. 
    1. In your Dockerfile you want to have at the top the following (replace with your image name as necessary)
        1. FROM pytorch/pytorch:1.12.1-cuda11.3-cudnn8-runtime
3. Enter the following into the prompt: 
    
    ```bash
    hare run -it --gpus device=0  -v "$(pwd)":/app pytorch/pytorch:1.12.1-cuda11.3-cudnn8-runtime bash
    ```
    
    1. hare is the docker command on Hex
    2. -it enables interactive, the final command “bash” opens the terminal. You need both.
    3. —gpus device=0 tells the image which gpu to use. Look on the usage page to find the one you want. See Tom’s docker help for how to use more than 1.
    4. -v "$(pwd)":/app is *essential* as it attaches your current working directory to the image’s folder /app. If you don’t do this, then you wont have any of your files.
    5. Replace the pytorch/pytorch:… with whatever image you have decided to use. 
4. You will now be on an interactive session within the base image where you can also view your files. You can now install all dependencies using “apt install” or “pip install”. Keep track of what you are installing, and for each command you put into the terminal make sure you add this to your Dockerfile with the word RUN, an example below:
    1. RUN pip install numpy
5. Continue with step 4 until you can run your desired file without error.
6. exit the container by typing: 
    
    ```bash
    exit
    ```
    
7. Find the name of the container by typing:
    
    ```bash
    hare me
    ```
    
8. Now save your container by typing the following: 
    
    ```bash
    hare commit <container name> <my username>/<my image name>
    ```
    
    (note you must save it as your username followed by whatever you want - so an example would be tc2034/tomsmujoco)
    
9. Remove the container (please always remember to remove containers - Tom makes this point many times)
    
    ```bash
    hare rm <container name>
    ```
    
10. At this point you have an image which you can use on Hex which will run your code! you can start it by just doing: 
    
    ```bash
    hare run -it --gpus device=0  -v "$(pwd)":/app <my username>/<my image name> bash
    ```
    
    Then you can run your code as you usually would within a terminal!
    
11. You will have also created a Dockerfile. Save this somewhere, and you will be able to reproduce this exact same image on a new computer if required.
