import logging
import os
import time

import requests
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Disable warning for not verifying self-signed cert
requests.packages.urllib3.disable_warnings()

### Installation specific variables need to be set here ###
EMBY_URL = ""
EMBY_PORT = ""
SSL_VERIFY=False
LIBRARY_PATHS = [

]
###########################################################

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class MediaEventHandler(FileSystemEventHandler):
    """Notify Emby of new media in libraries"""

    def on_any_event(self, event):
        """Check for desired event types and send api request"""
        super().on_any_event(event)

        if event.event_type in ["closed", "deleted", "moved"]:
            """
            Events to watch for:

            closed: a file opened for writing was closed
            deleted: a file or directory is deleted
            modified: a file or directory is modified
            """
            response = requests.post(
                url=f"{EMBY_URL}:{EMBY_PORT}/emby/Library/Refresh?",
                params={"api_key": os.environ.get("EMBY_API_KEY")},
                headers={"accept": "*/*"},
                data="",
                verify=SSL_VERIFY,
            )
            if response.ok:
                logger.info(f"Emby Library Scan: {event.event_type} - {event.src_path}")


def main() -> None:
    event_handler = MediaEventHandler()
    observer = Observer()
    for lib_path in LIBRARY_PATHS:
        observer.schedule(event_handler, lib_path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()


if __name__ == "__main__":
    main()
