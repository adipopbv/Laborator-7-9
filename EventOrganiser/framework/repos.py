from EventOrganiser.domain.entities import Command, Person, Event, Attendance
from EventOrganiser.domain.fields import Address, Date
from EventOrganiser.framework.json_tools import JsonSaver


class Repo:

    _items: list
    @property
    def items(self):
        return self._items
    @items.setter
    def items(self, value):
        self._items = value

    # ------------------

    def __init__(self, items: list):
        self.items = items

    def index_of(self, entity):
        try:
            return self.items.index(entity)
        except:
            raise Exception("Item not found in repo")

    def add(self, entity):
        self.items.append(entity)

    def modify(self, old_entity, new_entity):
        try:
            self.items[self.index_of(old_entity)] = new_entity
        except Exception as ex:
            raise Exception(ex)


class FileRepo(Repo, JsonSaver):

    _file_name: str
    @property
    def file_name(self):
        return self._file_name
    @file_name.setter
    def file_name(self, value):
        self._file_name = value

    # ----------------------------------

    def __init__(self, file_name: str, items: list):
        super().__init__(items)
        self.file_name = file_name
        # self.load_from_json()

    def save_to_json(self):
        file = open(self.file_name, "w")
        try:
            data_list = [item.to_json() for item in self.items]
            data = self.json.dumps(data_list, indent=4)
            file.write(data)
            file.close()
        except Exception as ex:
            file.close()
            raise Exception(ex)

    def load_from_json(self):
        pass


class CommandFileRepo(FileRepo):

    def load_from_json(self):
        file = open(self.file_name, "r")
        try:
            file_string = file.read()
            data = self.json.loads(file_string)

            commands = []
            for data_command in data:
                keys = []
                for data_key in data_command["keys"]:
                    keys.append(data_key)
                commands.append(Command(data_command["function"], data_command["description"], keys))

            self.items = commands
            file.close()
        except Exception as ex:
            file.close()
            raise Exception(ex)


class PersonFileRepo(FileRepo):

    def get_person_with_field_value(self, field, value):
        if field != "address":
            for person in self.items:
                try:
                    if getattr(person, field) == value:
                        return person
                except:
                    if getattr(person.address, field) == value:
                        return person
        raise Exception("No person with given field value")

    def load_from_json(self):
        file = open(self.file_name, "r")
        try:
            file_string = file.read()
            data = self.json.loads(file_string)

            persons = []
            for data_person in data:
                persons.append(Person(
                    data_person["id"],
                    data_person["name"],
                    Address(
                        data_person["address"]["city"],
                        data_person["address"]["street"],
                        data_person["address"]["number"]
                    )
                ))

            self.items = persons
            file.close()
        except Exception as ex:
            file.close()
            raise Exception(ex)


class EventFileRepo(FileRepo):

    def get_event_with_field_value(self, field, value):
        if field != "date":
            for event in self.items:
                try:
                    if getattr(event, field) == value:
                        return event
                except:
                    if getattr(event.date, field) == value:
                        return event
        raise Exception("No event with given field value")

    def load_from_json(self):
        file = open(self.file_name, "r")
        try:
            file_string = file.read()
            data = self.json.loads(file_string)

            events = []
            for data_event in data:
                events.append(Event(
                    data_event["id"],
                    Date(
                        data_event["date"]["day"],
                        data_event["date"]["month"],
                        data_event["date"]["year"]
                    ),
                    data_event["duration"],
                    data_event["description"]
                ))

            self.items = events
            file.close()
        except Exception as ex:
            file.close()
            raise Exception(ex)


class AttendanceFileRepo(FileRepo):

    def load_from_json(self):
        pass
