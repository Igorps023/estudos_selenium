import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
from pathlib import Path
import subprocess
import threading
import logging
logging.basicConfig(filename=Path(r'C:\Users\stree\OneDrive\Desktop\Selenium\SeleniumMoveFolder\myProgramLog.txt'), level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Handler(FileSystemEventHandler):
    def on_modified(self, event):

        #Lista todos os arquivos xlsx no diretorio
        xlsx_files = [file for file in os.listdir(folder_to_track) if file.endswith('.xlsx')]

        for filename in xlsx_files:            
            src = folder_to_track.joinpath(filename)
            new_dest = folder_destination.joinpath(filename)

            # Check if the file exists before attempting to move it
            if src.exists():
                # Filename_path = filename with Path library properties, used this for editing name
                filename_path = Path(filename)
                # Maximum number of attempts to check for stable file size
                max_attempts = 5
                for attempt in range(max_attempts):
                    # Wait for the file size to stabilize (indicating download completion)
                    initial_size = os.path.getsize(src)
                    time.sleep(4)  # Adjust the sleep duration as needed
                    final_size = os.path.getsize(src)

                    if initial_size == final_size:
                        timestamp = time.strftime('%Y_%m_%d_%H_%M_%S')
                        new_dest = folder_destination.joinpath(f'{filename_path.stem}_{timestamp}{filename_path.suffix}')

                        logging.info(f'Moved file: {src} to {new_dest}')
                        os.rename(src, new_dest)
                        break #Stop the loop
                    else:
                        logging.warning(f'File still in progress: {src}')

                    # If it's the last attempt, log a warning and move on
                    if attempt == max_attempts - 1:
                        logging.warning(f'File download not completed within the specified attempts: {src}')

            else:
                logging.warning(f'File not found: {src}')


def execute_selenium_job():
    # Execute another Python script at the end
    subprocess.run([sys.executable, Path(r'C:\Users\stree\OneDrive\Desktop\Selenium\SeleniumMoveFolder\SeleniumJob1.py')])


def watchdog_thread():
    # Watchdog logic
    observer = Observer()
    event_handler = Handler()
    observer.schedule(event_handler, folder_to_track, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt():
        observer.stop()

    observer.join()

if __name__ == "__main__":
    #Source
    folder_to_track = Path(r'C:\Users\stree\Downloads') #Antigo -> Path(r'C:\Users\stree\OneDrive\Desktop\PastaTesteMovert\Pasta1')
    #Destination
    folder_destination = Path(r'C:\Users\stree\OneDrive\Desktop\PastaTesteMovert\Pasta2')

    # Start Watchdog thread
    watchdog_thread = threading.Thread(target=watchdog_thread)

    # Start Selenium thread
    selenium_thread = threading.Thread(target=execute_selenium_job)

    # Start both threads concurrently
    watchdog_thread.start()
    selenium_thread.start()

    # Wait for both threads to finish
    watchdog_thread.join()
    selenium_thread.join()