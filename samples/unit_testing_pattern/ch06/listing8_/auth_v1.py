import datetime as dt
from dataclasses import dataclass
from pathlib import Path
from typing import List, Union


@dataclass
class AuthManager:
    _max_entries_per_file: int
    _directory_name: str

    @property
    def max_entries_per_file(self) -> int:
        return self._max_entries_per_file

    @property
    def directory_name(self) -> str:
        return self._directory_name

    def add_record(self, visitor_name: str, time_of_visit: dt.datetime) -> None:
        file_paths: List[Path] = [
            p for p in Path(self.directory_name).glob('*.txt') if p.is_file()
        ]

        record: str = f'{visitor_name};{time_of_visit.strftime("%Y-%m-%d %H:%M:%S")}'

        sorted_file_paths: List[Path] = self._sort_by_index(file_paths)

        if not sorted_file_paths:
            with open(Path(self._directory_name, 'audit_1.txt'), 'w') as f:
                f.write(record)
                f.write('\n')
                return

        last_file_path: Path = sorted_file_paths[-1]
        with open(last_file_path, 'r') as f:
            lines = f.readlines()

        if len(lines) < self.max_entries_per_file:
            with open(last_file_path, 'a+') as f:
                f.write(record)
                f.write('\n')
        else:
            index: int = self._get_index(last_file_path) + 1
            with open(Path(self._directory_name, f'audit_{index}.txt'), 'w') as f:
                f.write(record)
                f.write('\n')

    def _sort_by_index(self, files: List[Path]) -> List[Path]:
        return sorted(files, key=lambda p: self._get_index(p))

    @classmethod
    def _get_index(cls, filepath: Union[str, Path]) -> int:
        filename: str = Path(filepath).stem
        return int(filename.split('_')[-1])
