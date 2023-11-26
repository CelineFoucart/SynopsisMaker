import os
from pathlib import Path
import logging
import json
import shutil

from synopsis import Synopsis

PROJECTS_DIR = os.path.join(Path.home(), ".scenario-maker")
LOGGING_PATH = os.path.join(PROJECTS_DIR, "logging.log")
DATA_FILENAME = "data.json"

if not os.path.exists(PROJECTS_DIR):
    os.makedirs(PROJECTS_DIR)

logging.basicConfig(level=logging.INFO,
                    filename=LOGGING_PATH,
                    filemode="a",
                    format='%(asctime)s - %(levelname)s - %(message)s')


class Manager:
    """Class Manager handles data stored in the disk"""

    def __init__(self):
        self.data = {}
        self.set_data()

    def set_data(self) -> bool:
        """
        Retrieve all data from the dist
        :return: True in case of success or False
        """
        try:
            projects = {}

            dirs = [f for f in Path(PROJECTS_DIR).iterdir() if f.is_dir()]
            for path in dirs:
                uuid = path.name
                with open(path / DATA_FILENAME, "r") as f:
                    data = json.load(f)
                    data['uuid'] = uuid
                    projects[uuid] = Synopsis(**data)
            self.data = projects
            return True
        except Exception as e:
            logging.error(str(e))
            return False

    def get_one(self, uuid: str):
        """
        Retrieve one synopsis
        :param uuid: the unique identifier of the synopsis
        :return: the Synopsis in case of success
        """
        if uuid in self.data.keys():
            return self.data[uuid]
        logging.error(f"Try to open a non existing project {uuid}")
        return None

    def edit(self, uuid: str, data: dict) -> bool:
        """
        Edit a synopsis
        :param uuid: the unique identifier of the synopsis
        :param data: the new data
        :return: True in case of success or False
        """
        if uuid not in self.data.keys():
            logging.error(f"Try to edit a non existing project {uuid}")
            return False

        synopsis = self.data[uuid]

        if not isinstance(synopsis, Synopsis):
            logging.error(f"Invalid format for project {uuid}")
            return False

        synopsis.update(title=data['title'], description=data['title'])
        synopsis.set_events(events=data['events'])

        return Manager._persist_to_disk(synopsis)

    def create(self, data: dict) -> bool:
        """
        Create a synopsis.

        :param data: the data of the new Synopsis
        :return: True in case of success or False
        """
        synopsis = Synopsis(*data)
        self.data[synopsis.uuid] = synopsis
        os.makedirs(os.path.join(PROJECTS_DIR, synopsis.uuid))

        return Manager._persist_to_disk(synopsis)

    def delete(self, uuid: str) -> bool:
        """
        Delete a synopsis.
        :param uuid: the unique identifier of the synopsis
        :return: True in case of success or False
        """
        if uuid not in self.data.keys():
            logging.error(f"Try to delete a non existing project {uuid}")
            return False

        shutil.rmtree(os.path.join(PROJECTS_DIR, uuid), ignore_errors=True)
        del self.data[uuid]
        return True

    @staticmethod
    def _persist_to_disk(synopsis: Synopsis):
        """
        Save the synopsis on the disk
        :param synopsis: the entity to persist
        :return: True in case of success or False
        """
        try:
            with open(os.path.join(PROJECTS_DIR, synopsis.uuid, DATA_FILENAME), "w") as f:
                json.dump(synopsis.to_dict(), f, indent=4)
            return True
        except Exception as e:
            logging.error(str(e))
            return False


if __name__ == '__main__':
    m = Manager()
