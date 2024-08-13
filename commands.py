#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 00:55:55 2024

@author: ian
"""

import subprocess

# Handling different OS (linux/windows/mac)
# Handling different users


def conda_create(conda_shell, env_name):
    """
    Creates a conda environment, assuming conda is available
    """
    if "Jupyter" in env_name:
        packages = "-c conda-forge jupyterlab"
    elif "Napari" in env_name:
        packages = "-c conda-forge python=3.10 napari pyqt"
    else:
        packages = ""

    if "Cellpose" in env_name:
        command = "env create -f cellpose_environment.yml -y"
        full_command = f"source {conda_shell} && conda {command}"
    else:
        command = f"create -n {env_name} {packages} -y"
        full_command = f"source {conda_shell} && conda {command}"

    result = subprocess.run(
        ["bash", "-c", full_command], text=True, capture_output=True
    )

    return result


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
    print(result.stdout)
    return None


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
    conda_shell = os.path.join(home_dir, "miniconda3/etc/profile.d/conda.sh")
    print("Creating an environment...")
    conda_create(conda_shell, "cellpose_test")
    print("Environment created")
    print("Removing environment")
    conda_remove(conda_shell, "cellpose_test")
    print("Listing envs...")
    conda_env_list(conda_shell)

    print("Done")
