from os import scandir, rename
from os.path import splitext, exists, join
from shutil import move
from time import sleep

import logging

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Folders to track
source_dir = "C:\\Users\\jakeb\\Downloads"
dest_dir_music = "C:\\Users\\jakeb\\Downloads\\Music Downloads"
dest_dir_video = "C:\\Users\\jakeb\\Downloads\\Video Downloads"
dest_dir_image = "C:\\Users\\jakeb\\Downloads\\Image Downloads"
dest_dir_documents = "C:\\Users\\jakeb\\Downloads\\Document Downloads"
dest_dir_exes = "C:\\Users\\jakeb\\Downloads\\Exe Downloads"


image_extensions = [".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp"]

video_extensions = [".mp4", ".mp4v", ".m4v", ".avi", ".wmv"]

audio_extensions = [".m4a", ".flac", "mp3", ".wav", ".wma", ".aac"]

document_extensions = [".doc", ".docx", ".odt", ".pdf", ".xls", ".xlsx", ".ppt", ".pptx"]

exe_extensions = [".exe"]


def make_unique(dest, name):
    filename, extension = splitext(name)
    counter = 1
    # Add number to end of file if they exist, like downloading multiples
    while exists(f"{dest}/{name}"):
        name = f"{filename}({str(counter)}){extension}"
        counter += 1

    return name


def move_file(dest, entry, name):
    if exists(f"{dest}/{name}"):
        unique_name = make_unique(dest, name)
        oldName = join(dest, name)
        newName = join(dest, unique_name)
        rename(oldName, newName)
    move(entry, dest)


class MoverHandler(FileSystemEventHandler):
    # Runs whenever there is a change in the download's folder.
    def on_modified(self, event):
        with scandir(source_dir) as entries:
            for entry in entries:
                name = entry.name
                self.check_audio_files(entry, name)
                self.check_video_files(entry, name)
                self.check_image_files(entry, name)
                self.check_document_files(entry, name)
                self.check_exe_files(entry, name)

    def check_audio_files(self, entry, name):  # Method that checks all Audio Files
        for audio_extension in audio_extensions:
            if name.endswith(audio_extension) or name.endswith(audio_extension.upper()):
                move_file(dest_dir_music, entry, name)
                logging.info(f"Moved audio file: {name}")

    def check_video_files(self, entry, name):  # Method that checks all Video Files
        for video_extension in video_extensions:
            if name.endswith(video_extension) or name.endswith(video_extension.upper()):
                move_file(dest_dir_video, entry, name)
                logging.info(f"Moved video file: {name}")

    def check_image_files(self, entry, name):  # Method that checks all Image Files
        for image_extension in image_extensions:
            if name.endswith(image_extension) or name.endswith(image_extension.upper()):
                move_file(dest_dir_image, entry, name)
                logging.info(f"Moved image file: {name}")

    def check_document_files(self, entry, name):  # Method that checks all Document Files
        for documents_extension in document_extensions:
            if name.endswith(documents_extension) or name.endswith(documents_extension.upper()):
                move_file(dest_dir_documents, entry, name)
                logging.info(f"Moved document file: {name}")

    def check_exe_files(self, entry, name):  # Method that checks all Document Files
        for exe_extension in exe_extensions:
            if name.endswith(exe_extension) or name.endswith(exe_extension.upper()):
                move_file(dest_dir_exes, entry, name)
                logging.info(f"Moved Exe file: {name}")


# Initialization code from Watchdog - File change observation library
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = source_dir
    event_handler = MoverHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
