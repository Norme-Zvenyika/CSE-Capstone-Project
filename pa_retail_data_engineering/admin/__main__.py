# from database.Database import initialize_database
from data_pipeline.extract import Extractor
from data_pipeline.transform import Transformer
from data_pipeline.model import Model
from data_pipeline.load import Loader
from util import file_navigator
import os
import traceback

def main():
    db = None
    extracted_instance = None
    transformer = None
    model_obj = None

    # try:
    #     db = initialize_database()
    # except Exception as e:
    #     print(f"Error initializing the database: {e}")
    #     return

    try:
        while True:
            print("\nOptions:")
            print("1. Create Tables")
            print("2. Drop Tables")
            print("3. Extract Data")
            print("4. Transform Data")
            print("5. Load Data")
            print("6. Exit")
            print("7. Auto")

            choice = input("Enter your choice: ")

            if choice == '1':
                db.create_tables()
                db.create_procedures()
            elif choice == '2':
                db.drop_procedures()
                db.drop_tables()
            elif choice == '3':
                # replace this file with where your json are located.
                start_path = r"" # should be where the json files are located
                file_path = file_navigator.navigate_and_select_file(start_path)
                extracted_instance = Extractor(file_path).extracted_class()
            elif choice == '4':
                if extracted_instance is None:
                    print("Please extract data first.")
                else:
                    transformer = Transformer(extracted_instance)
                    print("\nTransform is complete.")
                    model_obj = Model(utilities_data=transformer.utilities_list)
            elif choice == '5':
                if model_obj is None:
                    print("Please transform data first.")
                else:
                    print("Start Loading: ")
                    Loader(model_obj,db)
                    print("\nLoad is complete.")
            elif choice == '6':
                break
            elif choice == '7':
                
                # auto_path = r"/mnt/c/Users/norma/OneDrive - Lehigh University/Desktop/BS BIOC Engineering/Spring 2024/CSE 281/Capstone/Individual Work/All 1999-2013"
                # years = list(range(1999, 2014))  # A more concise way to create the list of years

                # # Iterate through each year and process the JSON files
                # for year in years:
                #     year_path = os.path.join(auto_path, str(year))
                #     json_files = [f for f in os.listdir(year_path) if f.endswith('.json')]

                #     for json_file in json_files:
                #         file_path = os.path.join(year_path, json_file)
                #         print(f"\nProcessing file: {file_path}")

                #         # Extract, transform, and load the data from the JSON file
                #         extracted_instance = Extractor(file_path).extracted_class()
                #         transformer = Transformer(extracted_instance)
                #         print("\nTransform is complete.")
                #         model_obj = Model(utilities_data=transformer.utilities_list)
                #         Loader(model_obj, db)
                #         print("\nLoad is complete.")

                # 2014-2021 processing
                year_path = r"/mnt/c/Users/norma/OneDrive - Lehigh University/Desktop/BS BIOC Engineering/Spring 2024/CSE 281/Capstone/Individual Work/All 2014-2021"
                json_files = [f for f in os.listdir(year_path) if f.endswith('.json')]

                for json_file in json_files:
                    file_path = os.path.join(year_path, json_file)
                    print(f"\nProcessing file: {file_path}")

                    # Extract, transform, and load the data from the JSON file
                    extracted_instance = Extractor(file_path).extracted_class()
                    transformer = Transformer(extracted_instance)
                    print("\nTransform is complete.")
                    model_obj = Model(utilities_data=transformer.utilities_list)
                    Loader(model_obj, db)
                    print("\nLoad is complete.")

                print("All files have been processed.")
            else:
                print("Invalid choice. Please try again.")
    except Exception as e:
        traceback.print_exc() 
        print(f"Error: {e}")
    finally:
        if db and db.connection.is_connected():
            db.disconnect()

if __name__ == "__main__":
    main()
