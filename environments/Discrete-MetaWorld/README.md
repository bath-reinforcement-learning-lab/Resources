# Discete Meta-World

Please see the Meta-World environment here: https://meta-world.github.io/

However, the file here is a discrete version of meta-world. It wraps around the meta-world environment to create 11 discrete action buckets for the 4 different actions 

Importantly the wrapper is structured to be exactly the same as an open-ai gym environment. This is important as it allows training using stable-baselines3 (or your choice of baseline)

Within the discrete_metaworld.py file there is an example of how to run in a main.py script. I've also included a friendly plotting graphs file. 

Finally the Dockerfile is repeated here (it is the same as the one in the docker section)

Any issues contact me: tc2034@bath.ac.uk
