from pathlib import Path

from dupe_finder import find_duplicates


def test_find_duplicates_groups_matching_files_and_ignores_unique_files(tmp_path: Path):
    first = tmp_path / "first.txt"
    second = tmp_path / "nested" / "second.txt"
    unique = tmp_path / "unique.txt"
    second.parent.mkdir()
    first.write_text("same contents")
    second.write_text("same contents")
    unique.write_text("different")

    duplicates = find_duplicates(tmp_path)

    assert duplicates == [[first, second]]


def test_find_duplicates_can_include_empty_files(tmp_path: Path):
    first = tmp_path / "empty-a"
    second = tmp_path / "empty-b"
    first.touch()
    second.touch()

    assert find_duplicates(tmp_path) == [[first, second]]


def test_find_duplicates_returns_paths_in_stable_order(tmp_path: Path):
    names = ["z.txt", "a.txt", "m.txt"]
    for name in names:
        (tmp_path / name).write_text("duplicate")

    duplicates = find_duplicates(tmp_path)

    assert duplicates == [[tmp_path / "a.txt", tmp_path / "m.txt", tmp_path / "z.txt"]]
