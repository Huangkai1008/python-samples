import datetime as dt
from typing import List

from samples.unit_testing_pattern.ch06.listing8_.auth_v3 import (
    AuthManager,
    FileContent,
    FileUpdate,
)


class TestAuthV3:
    def test_a_new_file_is_created_when_the_current_file_overflows(self) -> None:
        auth_manager = AuthManager(3)
        files: List[FileContent] = [
            FileContent('audit_1.txt', []),
            FileContent(
                'audit_2.txt',
                [
                    'Peter; 2019-04-06 16:30:00',
                    'Jane; 2019-04-06 16:40:00',
                    'Jack; 2019-04-06 17:00:00',
                ],
            ),
        ]

        file_update = auth_manager.add_record(
            files, 'Alice', dt.datetime(2019, 4, 6, 18, 0, 0)
        )

        assert file_update == FileUpdate('audit_3.txt', 'Alice;2019-04-06 18:00:00')
