import datetime as dt
from dataclasses import dataclass
from pathlib import Path
from typing import AnyStr, List, Protocol, Union


class FileSystem(Protocol):
    def get_file_paths(self, directory_name: Union[str, Path]) -> List[Path]:
        ...

    def write(self, file_path: Path, content: AnyStr) -> None:
        ...

    def read_lines(self, file_path: Path) -> List[AnyStr]:
        ...


@dataclass
class AuthManager:
    _max_entries_per_file: int
    _directory_name: str

    file_system: FileSystem

    @property
    def max_entries_per_file(self) -> int:
        return self._max_entries_per_file

    @property
    def directory_name(self) -> str:
        return self._directory_name

    def add_record(self, visitor_name: str, time_of_visit: dt.datetime) -> None:
        file_paths: List[Path] = self.file_system.get_file_paths(
            Path(self.directory_name)
        )

        record: str = f'{visitor_name};{time_of_visit.strftime("%Y-%m-%d %H:%M:%S")}'

        sorted_file_paths: List[Path] = self._sort_by_index(file_paths)

        if not sorted_file_paths:
            self.file_system.write(Path(self._directory_name, 'audit_1.txt'), record)

        last_file_path: Path = sorted_file_paths[-1]
        lines = self.file_system.read_lines(last_file_path)

        if len(lines) < self.max_entries_per_file:
            lines.append(record)
            self.file_system.write(last_file_path, record)
        else:
            index: int = self._get_index(last_file_path) + 1
            self.file_system.write(
                Path(self._directory_name, f'audit_{index}.txt'), record
            )

    def _sort_by_index(self, files: List[Path]) -> List[Path]:
        return sorted(files, key=lambda p: self._get_index(p))

    @classmethod
    def _get_index(cls, filepath: Union[str, Path]) -> int:
        filename: str = Path(filepath).stem
        return int(filename.split('_')[-1])
