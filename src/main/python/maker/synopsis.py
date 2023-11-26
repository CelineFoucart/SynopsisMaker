from uuid import uuid4


class Synopsis:
    """Class Synopsis represents an entity"""

    def __init__(self, title: str, description: str, events: list = None, places: list = None, characters: list = None,
                 uuid: str = None):
        """Constructor for Synopsis"""

        self.title = title
        self.description = description
        self.events = []
        self.set_events(events)
        self.places = places if places else []
        self.characters = characters if characters else []
        self.uuid = uuid if uuid else str(uuid4())


    def __repr__(self) -> str:
        return f"{self.title} ({self.uuid})"

    def update(self, title: str, description: str) -> bool:
        self.title = title
        self.description = description
        return True

    def set_events(self, events: list = None):
        self.events = []

        if events:
            for event in events:
                self.events.append(Event(**event))

    def to_dict(self) -> dict:
        data = self.__dict__
        data['events'] = [event.__dict__ for event in self.events]
        data['places'] = [place.__dict__ for place in self.places]
        data['characters'] = [character.__dict__ for character in self.characters]
        del data['uuid']
        return data


class Event:
    """Class Synopsis represents an Event entity of a Synopsis"""

    def __init__(self, title: str, description: str, content: str, position: int = None):
        self.title = title
        self.description = description
        self.content = content
        self.position = position if position else 0

    def __repr__(self) -> str:
        return f"{self.title} (position: {self.position})"

    def validate(self) -> bool:
        return True

