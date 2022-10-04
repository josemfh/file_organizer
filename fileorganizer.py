"""
Library for handle files downloaded in a folder.

Move files as they are created in a folder to other selected folders

Classes available:
    - FileEventHandler: File event handler. Move files from then source folder to the selected folder
    - FileOrganizer: Read the configuration file and execute the file event handle schedule watch
"""
import json
import shutil
import logging
from time import sleep
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FileEventHandler(FileSystemEventHandler):
    ""

    def __init__(self, source_dir, directories_data, init_dir_process = True):
        self.source_dir = source_dir
        self.directories_data = directories_data
        if init_dir_process:
            self.processDirectory()

    def createFilename(self, dest, name, padding_number):
        """
            Create a unique name of the target file.

            Create a unique name of the target file if it already exists by adding a number to the original name.

            Arguments:
                - dest(string): Destination folder path
                - name(string): Original file name
                - padding_number(int): number of padding digits

            Return:
                - (string:) New full file path
        """
        # If file exist in dest, add number to the filename
        count = 0
        if dest.endswith('/'):
            dest = dest[:-1]
        filename, extension = name.split('.')
        while Path(f'{dest}/{name}').is_file():
            name = f'{filename}_{count:0>{padding_number}}.{extension}'
            count += 1
        return f'{dest}/{name}'


    def moveFile(self, dest, name, padding_number = 3):
        """
            Move file.

            Move file to the target folder. If it alredy exists, rename it.

            Arguments:
                - dest(string): Destination folder path
                - name(string): Original file name
                - padding_number(int): number of padding digits

            Return:

        """
        try:
            source_dir = self.source_dir.get('path')
            new_name = self.createFilename(dest, name, padding_number)
            shutil.move(f'{source_dir}/{name}', new_name)
            logging.info(f'File {source_dir}/{name} moved to {new_name}')
        except shutil.Error as error:
            logging.error(f'{error}')

    def getFileDest(self, extension):
        """
        Get destination folder path and padding number.

        Arguments:
            - extension(string): File extension

        Returns:
            - dest_dir, padding_number (tuple of string and number): Destination folder path and padding number
        """
        dest_dir = None
        padding_number= 3
        for directory_data in self.directories_data:
            dest_dir = directory_data.get('path')
            if Path(dest_dir).is_dir() and extension in directory_data.get('extensions'):
                padding_number = directory_data.get('padding_number')
                break

        return (dest_dir, padding_number)

    def processFile(self, file_name):
        """
        Process moving file
        Arguments:
            - file_name(string): File name
        Returns:
            None
        """
        if file_name.find('.') != -1:
            extension = file_name.split('.')[1]
            dest_dir, padding_number = self.getFileDest(extension)
            if dest_dir is not None:
                self.moveFile(dest_dir, file_name, padding_number)
            else:
                logging.error(f'The file {file_name} has a not recognized extension or target directory does not exist.')

    def processDirectory(self):
        """"
        Process moving directory
        Arguments:
            None
        Returns:
            None
        """
        directory_path = Path(self.source_dir.get('path'))
        files_in_path = directory_path.iterdir()
        for item in files_in_path:
            if item.is_file():
                self.processFile(item.name)


    def on_created(self, event):
        """ Called when a file or directory is created.

        Arguments:
            event (str): File system events
        Returns:
            None
        """
        if not event.is_directory:
            file_name = Path(event.src_path).name
            self.processFile(file_name)
        self.processDirectory()


class FileOrganizer(object):
    ""

    def __init__(self, config_file_path, init_dir_process = True):
        self.config_file_path = config_file_path
        self.source_dir = {}
        self.directories_data = []
        self.status = True
        self.status_message = 'Ok'

        self.loadSettingsData()
        self.checkDirectories()
        self.file_event_handler = FileEventHandler(self.source_dir, self.directories_data, init_dir_process)

    def checkDirectories(self):
        """Checking directories
        Checks directories, if they don't exist create them
        Arguments:
            None
        Returns:
            None
        """
        try:
            for directory_data in self.directories_data:
                directory = Path(directory_data['path'])
                if not directory.is_dir() and directory_data['create']:
                    directory.mkdir(parents=True)
                    logging.info(f'The {directory_data["path"]} directory was created')
        except Exception as e:
            logging.error(e)

    # Load settings data from configuration file
    def loadSettingsData(self):
        """ Load settings data
        Load settings data from configuration file
        Arguments:
            None
        Returns:
            None
        """

        if Path(self.config_file_path).is_file():
            with open(self.config_file_path,'r') as config_file:
                data = json.load(config_file)
                self.sleep_time = data.setdefault('sleep_time', 10)
                self.source_dir = data['source_dir'][:-1] if data['source_dir'].endwith('/') else data['source_dir']
                self.directories_data = tuple(data['directories'])
        else:
            self.status = False
            logging.error(f'The file {self.config_file_path} does not exist')
            self.status_message = f'The file {self.config_file_path} does not exist'

    def start(self):
        """ Starts the application
        Starts the observer
        Arguments:
            None
        Returns:
            None
        """
        if self.file_event_handler:
            observer = Observer()
            observer.schedule(self.file_event_handler, self.source_dir['path'], recursive = True)
            observer.start()
            logging.info('Observer started')
            logging.info(f'Source dir {self.source_dir["path"]}')
            try:
                while True:
                    sleep(self.sleep_time)
            except KeyboardInterrupt:
                observer.stop()
            observer.join()
            logging.info('Observer stopped')

if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.DEBUG,
                        format='[%(levelname)s] - %(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename='./file-organizer.log',
                        encoding='utf-8')
    except PermissionError:
        print('Permission denied to file')

    my_file_organizer = FileOrganizer('./config.json', True)
    if isinstance(my_file_organizer, FileOrganizer):
        my_file_organizer.start()
