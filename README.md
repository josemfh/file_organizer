# File organizer

Library for handle files downloaded in a directory.
Move files as they are created in a directory to other selected directories

## Installation

### Install dependencies

```bash
  pip3 install -r requirements.txt
```

### Turning it into a linux service with systemd

1. Create a file called /etc/systemd/system/file-organizer.service

```
[Unit]
Description=<description_about_your_project>
#Example for Description=file organizer

[Service]
User=<your user>
WorkingDirectory=<path/to/your/project/directory/containing/the/python/script>
ExecStart=path_of_python/virtualenv and your script file name

#Example for ExecStart=/home/your_user/.virtualenv/bin/python main.py
#Example for ExecStart=/path_of_pyton/python main.py
#replace /home/user/.virtualenv/bin/python with your virtualenv and main.py with your script name

Restart=always

[Install]
WantedBy=multi-user.target
```

2. Reload service files

```bash
sudo systemctl daemon-reload
```

3. Enable/Disable service on reboot

```bash
sudo systemctl enable/disable file-organizer.service
```

4. Start service

```bash
sudo systemctl start file-organizer.service
```

5. Check service status

```bash
sudo systemctl status file-organizer.service
```

## Usage/Examples

```python
import logging
from fileorganizer import FileOrganizer

logging.basicConfig(level = logging.INFO,
                    format = '[%(levelname)s] - %(asctime)s - %(message)s')

my_file_organizer = FileOrganizer('./config.json', True)
if not my_file_organizer.status:
    print(my_file_organizer.status_message)

my_file_organizer.start()
```

_config.json_: Configuration file

## Configuration file

### Parameters

- **sleep_time**: Time between check
- **source_dir**: Folder to check
- **name**: Directory's tag name
- **path**: Directory path
- **directories**: List of target directories
- **create**: Create the directory if it doesn't exist
- **padding_number**: If the file exists in the target directory, it is renamed to filename_number.extention. This parameter indicates that zeros (0) are added to the beginning of the number, until it reaches the specified length. Paddin_number = 3 -> filename_001.extension
- **extentions**: List of file extensions to be copied to the directory
- **directories**: List of target directories

### Example

```json
{
  "sleep_time": 10,
  "source_dir": {
    "name": "Download",
    "path": "/home/USER/Downloads"
  },
  "directories": [
    {
      "name": "images",
      "path": "/home/USER/Pictures",
      "create": true,
      "padding_number": 3,
      "extentions": ["jpg", "jpeg", "gif"]
    },
    {
      "name": "documents",
      "path": "/home/USER/Documents",
      "create": true,
      "padding_number": 3,
      "extentions": ["doc", "docx", "txt", "pdf"]
    },
    {
      "name": "audio",
      "path": "/home/USER/Audio/",
      "create": true,
      "padding_number": 3,
      "extentions": ["flac", "wav", "ogg", "mp3"]
    },
    {
      "name": "videos",
      "path": "/home/USER/Videos",
      "create": true,
      "padding_number": 3,
      "extentions": ["mp4", "avi", "mpeg"]
    }
  ]
}
```

## Log file example

[INFO] - 2022-09-07 19:48:24 - File /home/USER/send_to_folder/tmp/all/file68.mp4 moved to /home/USER/send_to_folder/tmp/vid/file68.mp4

[INFO] - 2022-09-07 19:48:24 - File /home/USER/send_to_folder/tmp/all/file64.txt moved to /home/USER/send_to_folder/tmp/doc/file64.txt

[ERROR] - 2022-09-07 19:48:24 - The file file67.pdf has a not recognized extention

[ERROR] - 2022-09-07 19:48:24 - The file file60.pdf has a not recognized extention

[INFO] - 2022-09-07 19:48:24 - File /home/USER/send_to_folder/tmp/all/file67.txt moved to /home/USER/send_to_folder/tmp/doc/file67.txt

[INFO] - 2022-09-07 19:48:24 - File /home/USER/send_to_folder/tmp/all/file61.txt moved to /home/USER/send_to_folder/tmp/doc/file61.txt

[INFO] - 2022-09-07 19:48:24 - File /home/USER/send_to_folder/tmp/all/file63.mp4 moved to /home/USER/send_to_folder/tmp/vid/file63.mp4

[INFO] - 2022-09-07 19:48:24 - File /home/USER/send_to_folder/tmp/all/file60.mp4 moved to /home/USER/send_to_folder/tmp/vid/file60.mp4

## License

[MIT](https://choosealicense.com/licenses/mit/)
