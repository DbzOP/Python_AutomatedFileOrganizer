import sqlite3

class DatabaseManager:
    def __init__(self, database_path):
        """Initialize and connect to the SQLite database, creating tables if needed."""
        self.conn = sqlite3.connect(database_path)
        self.cursor = self.conn.cursor()
        self.createTables()

    def createTables(self):
        """Create tables for settings, scheduled tasks, and file changes if they don't exist."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                date TEXT PRIMARY KEY,
                dir TEXT
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS scheduled_tasks (
                id INTEGER PRIMARY KEY,
                task_type TEXT,
                time_interval TEXT
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS file_changes (
                id INTEGER PRIMARY KEY,
                action TEXT,
                details TEXT
            )
        """)

    def loadSettings(self):
        """Retrieve user settings from the database or insert defaults if empty."""
        self.cursor.execute("SELECT * FROM settings")
        settings = dict(self.cursor.fetchall())
        # print("DB Settings below")
        # print(settings)

        if not settings: # If the settings table is empty
            default_settings = {
                "target_directory": r"C:\Users\perei\Desktop\projects\Python_AutomatedFileOrganizer\src\dbase\mydatabase.db",
                # Other default settings here
                }
            self.saveSettings(default_settings) # Save the default settings to the database
            return default_settings

        return settings

    def saveSettings(self, settings):
        """Save the provided settings to the database."""
        for key, value in settings.items():
            self.cursor.execute("INSERT OR REPLACE INTO settings (date, dir) VALUES (?, ?)", (key, value))
        self.conn.commit()

    def logChanges(self, changes):
        """Log changes made to files."""
        self.cursor.execute("INSERT INTO file_changes (action, details) VALUES (?, ?)", (changes['action'], changes['details']))
        self.conn.commit()

    def saveScheduledTask(self, task):
        """Save a scheduled task to the database."""
        self.cursor.execute("INSERT INTO scheduled_tasks (task_type, time_interval) VALUES (?, ?)", (task['task_type'], task['time_interval']))
        self.conn.commit()

    def removeScheduledTask(self, taskID):
        """Remove a specific scheduled task from the database using its ID."""
        self.cursor.execute("DELETE FROM scheduled_tasks WHERE id = ?", (taskID,))
        self.conn.commit()

    def listScheduledTasks(self):
        """Retrieve and return a list of all scheduled tasks from the database."""
        self.cursor.execute("SELECT * FROM scheduled_tasks")
        return self.cursor.fetchall()

    def closeConnection(self):
        """Close the connection to the database when the app is done with it."""
        self.conn.close()
