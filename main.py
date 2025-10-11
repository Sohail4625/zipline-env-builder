import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys


def check_strategy_file(strategy_file_path: str) -> None:
    print("Looking for the strategy file...")
    if Path(strategy_file_path).is_file() is False:
        print(
            "Error: File does not exist. "
            "Please provide valid file path, Ex: 'home/user/strategy.py'"
        )
        exit(1)
    print("Strategy file found")


def create_virtual_env(directory_path: Path) -> Path:
    venv_directory = directory_path / "venv"
    try:
        print("Creating a virtual environment...")
        subprocess.check_call([sys.executable, "-m", "venv", venv_directory])
        print("Virtual environment created")
        return venv_directory
    except subprocess.CalledProcessError as e:
        print("Failed to create a virtual environment", e)
        exit(1)


def install_dependencies(
    virtual_directory: Path, zipline_version: str, requirements_file_path: str
) -> None:
    env_pip_path = virtual_directory / "bin" / "pip"
    if zipline_version is None:
        zipline_version = "3.1.1"
    zipline_library = "zipline-reloaded" + f"=={zipline_version}"
    try:
        print("Installing libraries...")
        subprocess.check_call(
            [str(env_pip_path), "install", zipline_library, "ipython"]
        )
        if requirements_file_path is not None:
            print("Installing libraries from the provided requirements.txt file...")
            subprocess.check_call(
                [str(env_pip_path), "install", "-r", requirements_file_path]
            )
        print("Libraries successfully installed")
    except subprocess.CalledProcessError as e:
        print("Error installing the libraries ", e)
        exit(1)

def generate_run_script(project_dir: str, strategy_file: str) -> None:
    try:
        print("Generating run script...")
        bash_file = project_dir / "run_backtest.sh"
        source_file_name = Path(strategy_file).name
        bash_code = f"""#!/bin/bash
# Activate the virtual environment
source venv/bin/activate

# Run the zipline backtest
zipline run -f {source_file_name} --start 2016-1-1 --end 2018-1-1 --output /dev/null

echo "Backtest script finished."
        """
        with open(bash_file, "w") as f:
            f.write(bash_code)
        os.chmod(bash_file, 0o755)
        print("Script successfully generated as run_backtest.sh")
    except Exception as e:
        print("Error while generating run script", e)


def copy_strategy_file(source_path: str, destination_dir: Path) -> None:
    try:
        source_path_pathlib = Path(source_path)
        destination_path = destination_dir / source_path_pathlib.name
        print("Copying strategy file from source to destination..")
        shutil.copy(source_path, destination_path)
        print("File copied successfully")
    except FileNotFoundError as e:
        print("Error: File not found", e)
        exit(1)
    except PermissionError as e:
        print("Error: Permission denied", e)
        exit(1)
    except Exception as e:
        print("Error copying file", e)
        exit(1)


def create_new_directory(directory_name: str) -> Path:
    print(
        f"Creating new directory in the current directory with name {directory_name} ..."
    )
    try:
        current_directory = Path.cwd()
        new_directory = current_directory / directory_name  # Creating new directory
        new_directory.mkdir(parents=True)
    except FileExistsError:
        print(
            f"The directory '{directory_name}' already exists. Please provide another name"
        )  # Exit if directory already exists and notify user
        exit(1)
    except OSError:
        print(
            "Failed to create directory. "
            "Please provide a valid name in the arguments, Ex: test_dir"
        )
        exit(1)
    print("New directory created")
    return new_directory


def main() -> None:
    parser = argparse.ArgumentParser(description="Zipline Environment Builder")

    parser.add_argument(
        "--strategy-file", type=str, help="Location of strategy file", required=True
    )
    parser.add_argument(
        "--name", type=str, help="Name of the testing directory", required=True
    )
    parser.add_argument(
        "--zipline-version", type=str, help="Version of zipline to be used"
    )
    parser.add_argument(
        "--requirements",
        type=str,
        help="Location of requirements.txt file to be installed into the environment",
    )
    args = parser.parse_args()
    check_strategy_file(args.strategy_file)
    new_directory_path = create_new_directory(args.name)
    virtual_directory_path = create_virtual_env(directory_path=new_directory_path)
    install_dependencies(
        virtual_directory=virtual_directory_path,
        zipline_version=args.zipline_version,
        requirements_file_path=args.requirements,
    )
    copy_strategy_file(args.strategy_file, new_directory_path)
    generate_run_script(new_directory_path, args.strategy_file)


if __name__ == "__main__":
    main()
