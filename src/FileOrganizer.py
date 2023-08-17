import os
import shutil
import zipfile
import mimetypes
from DatabaseManager import DatabaseManager
from datetime import datetime

class FileOrganizer:
    def __init__(self, settings, database_path, currentpath):
        """Initialize with user settings and connect to the database."""
        self.currentpath = currentpath
        self.settings = settings
        self.target_directory = settings.get("target_directory", currentpath)
        self.db_manager = DatabaseManager(database_path)
        self.classified_files = {}
        self.scanAndClassify()

    def scanAndClassify(self):
        """Traverse the target directory and classify files by type."""
        mimetypes.add_type('application/x-blender', '.blend') # Add MIME type for Blender files

        if not os.path.exists(self.target_directory):
            print("The target directory does not exist!")
            return

        if not os.path.isdir(self.target_directory):
            print("The target directory is not a directory!")
            return

        for root, dirs, files in os.walk(self.target_directory):
            for file in files:
                self.classifyFile(os.path.join(root, file))

    def classifyFile(self, file_path):
        """Classify a file by its MIME type."""
        file_type, _ = mimetypes.guess_type(file_path)
        self.classified_files[file_path] = file_type.split("/")[0] if file_type else "unknown"

    def organizeFiles(self):
        """Organize the classified files into folders by type and log changes."""
        current_date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for file_path, file_type in self.classified_files.items():
            self.moveFileToTypeFolder(file_path, file_type)

        self.settings[current_date_time] = self.currentpath
        self.db_manager.saveSettings(self.settings)

        return "Files organized successfully!"

    def moveFileToTypeFolder(self, file_path, file_type):
        """Move a file to its corresponding type folder."""
        type_folder = os.path.join(self.target_directory, file_type)
        os.makedirs(type_folder, exist_ok=True)
        shutil.move(file_path, os.path.join(type_folder, os.path.basename(file_path)))
        self.db_manager.logChanges({'action': 'move', 'details': file_path})

    def zipFiles(self, files_to_zip):
        """Compress the specified files/folders and log changes."""
        with zipfile.ZipFile('files.zip', 'w') as zipf:
            for file in files_to_zip:
                zipf.write(file)
                self.db_manager.logChanges({'action': 'zip', 'details': file})
        return "Files zipped successfully!"

    def unzipFiles(self, files_to_unzip):
        """Decompress the specified files/folders and log changes."""
        with zipfile.ZipFile(files_to_unzip, 'r') as zip_ref:
            zip_ref.extractall(self.target_directory)
            self.db_manager.logChanges({'action': 'unzip', 'details': files_to_unzip})
        return "Files unzipped successfully!"

    def close(self):
        """Close the database connection when done."""
        self.db_manager.closeConnection()
