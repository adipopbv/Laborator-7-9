from ui.gui.consoles import Console
from framework.repos import CommandsRepo
from domain.entities import Id, Function, Command

class Client:
    
    def __init__(self, service):
        self._service = service
        self._gui = Console()
        self._commands = CommandsRepo(
            Command(Id("1"), Function(self.add_person_to_repo)),
            Command(Id("2"), Function(self.add_event_to_repo)),
            Command(Id("3"), Function(self.modify_person_from_repo)),
            Command(Id("4"), Function(self.modify_event_from_repo)),
        )

    def get_service(self):
        return self._service

    def get_gui(self):
        return self._gui

    def get_commands(self):
        return self._commands

    #---------------------------

    def read(self, prompt):
        """
        reads input from the user
        
        Args:
            prompt (str): text to be outputted before getting input
        
        Returns:
            str: input text
        """
        text = self.get_gui().read(prompt)
        return text

    def read_command(self):
        """
        reads input command from the user
        
        Returns:
            list: a command
        """
        try:
            text = self.read("Please input a command: ")
            text = text.strip()
            text = text.split()
            return text[0]
        except Exception as ex:
            self.write_exception(ex)   
            return self.read_command()         

    def write(self, message):
        """
        writes output message to the user
        
        Args:
            message (str): output text
        """
        self.get_gui().write(message)

    def write_success(self):
        self.write("Operation successful!")

    def write_exception(self, exception):
        """
        writes exception to the user
        
        Args:
            exception (Exception): an exception
        """
        self.write("Error: " + str(exception))

    #---------------------------

    def add_person_to_repo(self):
        """
        reads and adds a person to the repo
        """
        try:
            self.write("Please input a person:")
            self.get_service().add_person_to_repo(
                self.get_service().get_persons(), 
                self.read("Id: "),  
                self.read("Name: "),
                self.read("Adress \n    City: "),
                self.read("    Street: "),
                self.read("    Number: ")
            )
            self.write_success()
        except Exception as ex:
            self.write_exception(ex)

    def add_event_to_repo(self):
        """
        reads and adds an event to the repo
        """
        try:
            self.write("Please input an event:")
            self.get_service().add_event_to_repo(
                self.get_service().get_events(),
                self.read("Id: "),
                self.read("Date \n    Day: "),
                self.read("    Month: "),
                self.read("    Year: "),
                self.read("Duration \n    Hours: "),
                self.read("    Minutes: "),
                self.read("Description: ")
            )
            self.write_success()
        except Exception as ex:
            self.write_exception(ex)

    def modify_person_from_repo(self):
        """
        reads an id and a person's new data to change to
        """
        try:
            self.write("Please input a person's id:")
            self.get_service().modify_person_from_repo(
                self.get_service().get_persons(),
                self.read("Id: "),
                self.read("Please input the modified person's data:\nId: "),  
                self.read("Name: "),
                self.read("Adress \n    City: "),
                self.read("    Street: "),
                self.read("    Number: ")
            )
            self.write_success()
        except Exception as ex:
            self.write_exception(ex)

    def modify_event_from_repo(self):
        try:
            self.write("Please input an event's id:")
            self.get_service().modify_event_from_repo(
                self.get_service().get_events(),
                self.read("Id: "),
                self.read("Please input the modified event's data:\nId: "),
                self.read("Date \n    Day: "),
                self.read("    Month: "),
                self.read("    Year: "),
                self.read("Duration \n    Hours: "),
                self.read("    Minutes: "),
                self.read("Description: ")
            )
            self.write_success()
        except Exception as ex:
            self.write_exception(ex)

    def run(self):
        """
        application main loop
        """
        while True:
            try:
                command = self.read_command()
                self.get_commands().get_command_with_id_value(command[0]).run()
            except Exception as ex:
                self.write_exception(ex)