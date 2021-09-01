from unittest import mock
from unittest.mock import Mock

from samples.unit_testing_pattern.ch05.controller import Controller


@mock.patch('samples.unit_testing_pattern.ch05.email.EmailGateway')
@mock.patch('samples.unit_testing_pattern.ch05.database.Database')
class TestController:
    def test_sending_a_greeting_email(
        self, mock_email_gateway: Mock, mock_database: Mock
    ) -> None:
        # The email gateway is mock.
        controller: Controller = Controller(mock_email_gateway, mock_database)

        controller.greet_user('user@email.com')

        mock_email_gateway.send_greetings_email.assert_called_once_with(
            'user@email.com'
        )

    def test_creating_a_report(
        self, mock_email_gateway: Mock, mock_database: Mock
    ) -> None:
        # The database is stub.
        mock_database.get_number_of_users.return_value = 10
        controller: Controller = Controller(mock_email_gateway, mock_database)

        report = controller.create_report()

        assert report.number_of_users == 10
