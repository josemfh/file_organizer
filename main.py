import logging
from fileorganizer import FileOrganizer

logging.basicConfig(level = logging.INFO, 
                    format = '[%(levelname)s] - %(asctime)s - %(message)s')

my_file_organizer = FileOrganizer('./config.json', True)
if not my_file_organizer.status:
    print(my_file_organizer.status_message)

my_file_organizer.start()



