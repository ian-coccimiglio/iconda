#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 00:55:55 2024

@author: ian
"""

import subprocess
import platform

# Handling different OS (linux/windows/mac)
# Handling different users


def get_conda_shell():
    system = platform.system()
    if system == "Windows":
        home_dir = os.path.expanduser("~")
        return os.path.join(home_dir, "Miniconda3", "Scripts", "activate.bat")
    elif system == "Linux" or system == "Darwin":
        home_dir = os.path.expanduser("~")
        return os.path.join(home_dir, "miniconda3/etc/profile.d/conda.sh")
    else:
        raise NotImplementedError(f"Unsupported OS: {system}")


def conda_env_exists(conda_shell, env_name):
    """
    Checks if a conda environment exists.
    """
    system = platform.system()
    if system == "Windows":
        full_command = f"call {conda_shell} && conda env list"
        result = subprocess.run(
            ["cmd.exe", "/c", full_command],
            text=True,
            capture_output=True,
            check=True,
        )
    else:
        full_command = f"source {conda_shell} && conda env list"
        result = subprocess.run(
            ["bash", "-c", full_command],
            text=True,
            capture_output=True,
            check=True,
        )

    envs = result.stdout.splitlines()
    for env in envs:
        if env_name in env:
            return True
    return False


def conda_create(conda_shell, env_name, from_environment=False):
    """
    Creates a conda environment, assuming conda is available
    """
    if "jupyter" in env_name:
        packages = "-c conda-forge jupyterlab"
    elif "napari" in env_name:
        packages = "-c conda-forge python=3.10 napari pyqt"
    else:
        packages = ""

    if from_environment == False:
        command = f"create -n {env_name} {packages} -y"
    else:
        environment = get_environment(env_name)
        command = f"env create -f {environment} -y"
    full_command = f"source {conda_shell} && conda {command}"

    result = subprocess.run(
        ["bash", "-c", full_command], text=True, capture_output=True
    )

    return result


def get_environment(env_name):
    environment = None
    if env_name == "Cellpose":
        environment = "cellpose_environment.yml"
    return environment


def run_in_conda_env(conda_shell, env_name, command):
    full_command = (
        f"source {conda_shell} && conda activate {env_name} && {command}"
    )
    result = subprocess.run(
        ["bash", "-c", full_command],
        text=True,
    )
    return result.stdout, result.stderr


def conda_env_list(conda_shell):
    """
    Lists all conda environments, assuming conda is available
    """

    full_command = f"source {conda_shell} && conda env list"
    result = subprocess.run(
        ["bash", "-c", full_command], text=True, capture_output=True
    )
    return result.stdout


def conda_remove(conda_shell, env_name):
    """
    Removes a conda environment, assuming conda is available
    """
    command = f"env remove -n {env_name} -y"
    full_command = f"source {conda_shell} && conda {command}"
    result = subprocess.run(
        ["bash", "-c", full_command], text=True, capture_output=True
    )
    return result


if __name__ == "__main__":
    import os

    home_dir = os.path.expanduser("~")
    conda_shell = get_conda_shell()
    print("Creating an environment...")
    conda_create(conda_shell, "cellpose_test")
    print("Environment created")
    print("Removing environment")
    conda_remove(conda_shell, "cellpose_test")
    print("Listing envs...")
    conda_env_list(conda_shell)

    print("Done")
