import torch
import importlib.util
import gymnasium as gym


def is_package_installed(package_name):
    """Check if a Python package is installed."""
    spec = importlib.util.find_spec(package_name)
    return spec is not None


def check_pytorch_installation():
    print("Checking PyTorch installation...")
    # Check PyTorch installation
    try:
        print(f"PyTorch version: {torch.__version__}")
    except ImportError:
        print("PyTorch is not installed.")
        return

    if torch.cuda.is_available():
        print("CUDA is available. PyTorch can use GPU!")
        # Check GPU accessibility by moving a tensor to GPU
        try:
            x = torch.tensor([1.0])
            x = x.cuda()
            print("Successfully moved tensor to GPU:", x)
            print("GPU Details:")
            print(f"Number of GPUs available: {torch.cuda.device_count()}")
            for i in range(torch.cuda.device_count()):
                print(f"  GPU {i}: {torch.cuda.get_device_name(i)}")
        except Exception as e:
            print("An error occurred while moving tensor to GPU:", e)
    else:
        print("CUDA is not available. PyTorch cannot use GPU.")


def check_other_packages():
    packages = ["tqdm", "tensorboard", "gymnasium", "numpy", "tyro"]
    print("Checking for other required packages...")
    for package in packages:
        if is_package_installed(package):
            print(f"{package} is installed.")
        else:
            print(f"{package} is not installed.")


def test_mujoco_installation():
    print("Testing mujoco installation by running an episode of Ant-v4...")

    # Initialize the environment
    env = gym.make("Ant-v4")

    # Reset the environment to start
    observation = env.reset()

    # Run one episode
    done = False
    while not done:
        action = env.action_space.sample()  # Random action
        observation, reward, terminated, truncated, _ = env.step(action)
        done = terminated or truncated
        # print(f"Observation: {observation}, Reward: {reward}")

    # Close the environment
    env.close()


if __name__ == "__main__":
    check_pytorch_installation()
    check_other_packages()
    test_mujoco_installation()
