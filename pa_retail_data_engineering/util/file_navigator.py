import os

def list_directory(path):
    print("\nCurrent directory:", path)
    print("\nChoose an option:")
    print("0: Go back")
    files_and_dirs = os.listdir(path)
    for i, item in enumerate(files_and_dirs, start=1):
        print(f"{i}: {item}")
    return files_and_dirs

def navigate_and_select_file(start_path):
    current_path = start_path
    history = [start_path]

    while True:
        files_and_dirs = list_directory(current_path)

        choice = input("\nEnter your choice (number): ").strip()
        if not choice.isdigit() or not 0 <= int(choice) <= len(files_and_dirs):
            print("Invalid choice. Please try again.")
            continue

        choice = int(choice)
        if choice == 0:
            if len(history) > 1:
                history.pop()
                current_path = history[-1]
            else:
                print("You are already at the root directory.")
        else:
            selected_item = files_and_dirs[choice - 1]
            selected_path = os.path.join(current_path, selected_item)
            if os.path.isdir(selected_path):
                current_path = selected_path
                history.append(current_path)
            else:
                print(f"\nYou selected the file: {selected_path}")
                return selected_path
