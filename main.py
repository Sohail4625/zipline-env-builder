import argparse
from pathlib import Path


def check_strategy_file(strategy_file_path: str) -> None:
    print("Looking for the strategy file...")
    if Path(strategy_file_path).is_file() is False:
        print(
            "Error: File does not exist. "
            "Please provide valid file path, Ex: 'home/user/strategy.py'"
        )
        exit(1)
    print("Strategy file found")


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
    args = parser.parse_args()
    check_strategy_file(args.strategy_file)
    create_new_directory(args.name)


if __name__ == "__main__":
    main()
