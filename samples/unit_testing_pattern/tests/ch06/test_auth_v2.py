import datetime as dt
from pathlib import Path
from typing import List, Union
from unittest import mock
from unittest.mock import Mock

from samples.unit_testing_pattern.ch06.listing8_.auth_v2 import AuthManager


@mock.patch('samples.unit_testing_pattern.ch06.listing8_.auth_v2.FileSystem')
class TestAuthV2:
    def test_a_new_file_is_created_when_the_current_file_overflows(
        self, mock_file_system: Mock
    ) -> None:
        def get_file_paths(directory_name: Union[str, Path]) -> List[Path]:
            return [
                Path(directory_name, 'audit_1.txt'),
                Path(directory_name, 'audit_2.txt'),
            ]

        def read_lines() -> List[str]:
            return [
                'Peter; 2019-04-06 16:30:00',
                'Jane; 2019-04-06 16:40:00',
                'Jack; 2019-04-06 17:00:00',
            ]

        mock_file_system.get_file_paths.side_effect = get_file_paths
        mock_file_system.read_lines.return_value = read_lines()
        auth_manager = AuthManager(3, 'audits', mock_file_system)

        auth_manager.add_record('Alice', dt.datetime(2019, 4, 6, 18, 0, 0))

        mock_file_system.write.assert_called_with(
            Path('audits', 'audit_3.txt'), 'Alice;2019-04-06 18:00:00'
        )
