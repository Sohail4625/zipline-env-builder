import argparse
from pathlib import Path
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


if __name__ == "__main__":
    main()
