"""
entry point for the data pipeline — lets a user interactively
extract a JSON file, transform it (year-specific logic), and
optionally load it into the database.
"""

import argparse
import traceback
import os

from data_pipeline.extract import Extractor
from data_pipeline.transform import Transform
from data_pipeline.model import Model
from data_pipeline.load import Loader
from util import file_navigator


def extract_data(start_path: str):
    """
    prompt user to select a file and return:
        - the loaded JSON
        - the directory name (used to extract year)
    """
    file_path, year_dir = file_navigator.navigate_and_select_file(start_path)
    print("\nExtract in progress...")
    data = Extractor(file_path).load()
    print("Extract completed.")
    return data, year_dir


def transform_data(raw_data, year: int):
    """run the year-specific transform and wrap result in a Model object"""
    print("\nTransform in progress...")
    transformed = Transform(raw_data, year).run()
    print("Transform completed.")
    return Model(utilities_data=transformed)


def load_data(model_obj, output_path):
    """send transformed model to the Loader"""
    print("\nLoading in progress...")
    Loader(model_obj, output_path)
    print("Load completed.")


def run_batch(start_path, output_path):
    """
    automatically extract, transform, and load all JSON files in subdirectories of start_path
    """
    print("batch mode enabled...\n")

    for subdir in sorted(os.listdir(start_path)):
        full_dir = os.path.join(start_path, subdir)
        if not os.path.isdir(full_dir):
            continue

        # determine year
        if subdir.isdigit():
            year = int(subdir)
        elif subdir.lower() == "default_providers":
            year = 0
        else:
            print(f"skipping unrecognized directory: {subdir}")
            continue

        print(f"\nYear: {year}")

        for filename in os.listdir(full_dir):
            if not filename.endswith(".json"):
                continue

            file_path = os.path.join(full_dir, filename)

            try:
                data = Extractor(file_path).load()
                model = Transform(data, year).run()
                model_obj = Model(utilities_data=model)
                Loader(model_obj, output_path)
            except Exception as err:
                print(f"error while processing {file_path}: {err}")
                traceback.print_exc()
                continue



def main(start_path, output_path):
    """
    interactive CLI for extract -> transform -> load

    parameters
    start_path : str
        directory from which the user will choose the JSON file
    """
    raw_data = None
    model_obj = None

    try:
        while True:
            print("\nOptions:")
            print("1. Extract data")
            print("2. Transform data")
            print("3. Load data")
            print("4. Exit")

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                raw_data, detected_year = extract_data(start_path)

            elif choice == "2":
                if raw_data is None:
                    print("please extract data first.")
                    continue
                year_str = detected_year

                # default providers is a collection of years hence why I use the directory name.
                # if the directory name is default_only, year should be set to zero
                if not year_str.isdigit() and year_str.lower() != "default_providers":
                    print(f"could not determine year from path: {start_path}")
                    continue
                year = int(year_str) if year_str.isdigit() else 0
                model_obj = transform_data(raw_data, year)

            elif choice == "3":
                if model_obj is None:
                    print("please transform data first.")
                    continue
                load_data(model_obj, output_path)

            elif choice == "4":
                print("exiting...")
                break

            else:
                print("invalid choice. please try again.")

    except FileNotFoundError as err:
        print(f"file not found: {err}")
    except ValueError as err:
        print(f"value error: {err}")
    except Exception as err:                         # catch-all for unexpected issues
        traceback.print_exc()
        print(f"unexpected error: {err}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="run the data-pipeline CLI")
    parser.add_argument(
        "--start-path",
        type=str,
        required=True,
        help="directory containing JSON files",
    )
    parser.add_argument(
        "--output-path",
        type=str,
        required=True,
        help="directory where CSVs will be saved",
    )
    parser.add_argument(
        "--auto-load-all",
        action="store_true",
        help="automatically process all JSON files in all subdirectories"
    )

    args = parser.parse_args()

    if args.auto_load_all:
        run_batch(args.start_path, args.output_path)
    else:
        main(args.start_path, args.output_path)
