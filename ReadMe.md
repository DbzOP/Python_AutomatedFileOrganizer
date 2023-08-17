# Automated File Organizer (WIP)

## Author: Michael Pereira

Automated File Organizer is a Python application designed to manage and organize files on your system. It provides functionalities to classify, organize, zip, and unzip files, and it integrates with an SQLite database to manage user settings and log file changes.

Michael Pereira developed this project with the assistance of AI to ensure code quality and efficiency.

## Components

The project consists of three main classes:

### 1. UserInterface

This class provides the graphical user interface (GUI) for the application, allowing users to interact with the system. It includes buttons and layouts to navigate and perform actions like organizing and zipping files.

### 2. FileOrganizer

The FileOrganizer class is responsible for scanning, classifying, and organizing files based on their types. It also handles file compression and decompression.

### 3. DatabaseManager

The DatabaseManager class manages the SQLite database connection and provides methods to create tables, load and save settings, log file changes, and manage scheduled tasks.

## How to Use

1. **Clone the Repository**: Clone the project repository to your local machine.
2. **Install Dependencies**: Make sure to have PyQt5 installed to run the GUI.
3. **Run the Application**: Execute the main file to launch the GUI.
4. **Interact with the GUI**: Use the buttons and options in the GUI to organize and manage your files.

## Features

- **File Classification**: Classify files based on their MIME types.
- **File Organization**: Organize files into folders by type.
- **File Compression**: Zip and unzip files as needed.
- **User Settings**: Load and save user settings from/to the database.
- **Logging**: Log file changes and actions in the database.

## Acknowledgments

I used ChatGPT for assisting in the development process, providing insights, and helping with code refactoring.

## Contact

For any inquiries or collaboration, please contact Michael Pereira at [email@example.com](mailto:pereiramichael128@gmail.com).

