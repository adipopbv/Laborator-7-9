from ui.clients import Client
from business.services import Service
from framework.repos import Repo
from framework.validators import Validator
from tests import Tests

tests = Tests()
persons = Repo()
events = Repo()
validator = Validator()
service = Service(persons, events, validator)
client = Client(service)

tests.run_all()
client.run()