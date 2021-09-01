import datetime as dt
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Union


@dataclass(frozen=True)
class FileUpdate:
    file_name: str
    content: str

    def __eq__(self, other: 'FileUpdate') -> bool:
        return self.file_name == other.file_name and self.content == other.content


@dataclass(frozen=True)
class FileContent:
    file_name: str
    lines: List[str]


@dataclass
class Persister:
    @classmethod
    def read_directory(cls, directory_name: Union[str, Path]) -> List[FileContent]:
        file_paths = [p for p in Path(directory_name).glob('*.txt') if p.is_file()]
        file_contents = []
        for path in file_paths:
            with open(path) as f:
                lines = f.readlines()

            content = FileContent(path.name, lines)
            file_contents.append(content)
        return file_contents

    @classmethod
    def apply_update(
        cls, directory_name: Union[str, Path], file_update: FileUpdate
    ) -> None:
        file_path = Path(directory_name, file_update.file_name)
        with open(file_path, 'w') as f:
            f.write(file_update.content)


@dataclass
class AuthManager:
    _max_entries_per_file: int

    @property
    def max_entries_per_file(self) -> int:
        return self._max_entries_per_file

    def add_record(
        self, files: List[FileContent], visitor_name: str, time_of_visit: dt.datetime
    ) -> FileUpdate:
        sorted_files: List[FileContent] = self._sort_by_index(files)
        record: str = f'{visitor_name};{time_of_visit.strftime("%Y-%m-%d %H:%M:%S")}'

        if not sorted_files:
            return FileUpdate('audit_1.txt', record)

        current_file: FileContent = sorted_files[-1]
        lines = current_file.lines

        if len(lines) < self.max_entries_per_file:
            lines.append(record)
            return FileUpdate(current_file.file_name, '\n'.join(lines))
        else:
            index: int = self._get_index(current_file.file_name) + 1
            return FileUpdate(f'audit_{index}.txt', record)

    def _sort_by_index(self, files: List[FileContent]) -> List[FileContent]:
        return sorted(files, key=lambda p: self._get_index(p.file_name))

    @classmethod
    def _get_index(cls, filepath: Union[str, Path]) -> int:
        filename: str = Path(filepath).stem
        return int(filename.split('_')[-1])


@dataclass
class ApplicationService:
    _directory_name: str
    _max_entries_per_file: int
    _persister: Persister = field(default_factory=Persister)
    _auth_manager: AuthManager = field(init=False)

    def __post_init__(self) -> None:
        self._auth_manager = AuthManager(self._max_entries_per_file)

    def add_record(self, visitor_name: str, time_of_visit: dt.datetime) -> None:
        files: List[FileContent] = self._persister.read_directory(self._directory_name)
        file_update: FileUpdate = self._auth_manager.add_record(
            files, visitor_name, time_of_visit
        )
        self._persister.apply_update(self._directory_name, file_update)
