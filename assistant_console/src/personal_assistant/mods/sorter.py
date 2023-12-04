import os
import shutil
from mods.log_config import get_logger_error


logger = get_logger_error(__name__)


def sort_files():
    while True:
        folder_path = input(
            "Enter the absolute path of the folder to sort (example: C:\Desktop\project) o press Enter to skip: "
        )
        folder_path = folder_path.strip()

        categorized_files = {}

        if folder_path == "":
            return "Operation skipped"

        try:
            for file_name in os.listdir(folder_path):
                if os.path.isfile(os.path.join(folder_path, file_name)):
                    if file_name in ("butler.py", "backup.dat"):
                        continue

                    file_extension = os.path.splitext(file_name)[1]
                    category = "Other"
                    if file_extension in (".jpg", ".png", ".gif"):
                        category = "Images"
                    elif file_extension in (".doc", ".docx", ".pdf"):
                        category = "Documents"
                    elif file_extension in (".mp4", ".avi", ".mov"):
                        category = "Videos"

                    if category not in categorized_files:
                        categorized_files[category] = []

                    categorized_files[category].append(file_name)

            if not categorized_files:
                return "No files found for sorting."

            for category in categorized_files.keys():
                category_folder = os.path.join(folder_path, category)
                os.makedirs(category_folder, exist_ok=True)

            for category, files in categorized_files.items():
                category_folder = os.path.join(folder_path, category)
                for file_name in files:
                    source_path = os.path.join(folder_path, file_name)
                    destination_path = os.path.join(category_folder, file_name)
                    shutil.move(source_path, destination_path)

            return "File sorting completed successfully."

        except:
            logger.error("Wrong pass")
            print("Invalid folder path, try one more time")


if __name__ == "__main__":
    print(sort_files())
