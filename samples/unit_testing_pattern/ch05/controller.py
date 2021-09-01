from dataclasses import dataclass

from samples.unit_testing_pattern.ch05.database import Database
from samples.unit_testing_pattern.ch05.email import EmailGateway
from samples.unit_testing_pattern.ch05.report import Report


@dataclass(frozen=True)
class Controller:
    email_gateway: EmailGateway
    database: Database

    def greet_user(self, user_email: str) -> None:
        self.email_gateway.send_greetings_email(user_email)

    def create_report(self) -> Report:
        number_of_users: int = self.database.get_number_of_users()
        return Report(number_of_users)
