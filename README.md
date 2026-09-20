# Folder Dupe Finder

A small, dependency-free Python CLI that recursively finds duplicate regular files by SHA-256 content hash.

## Usage

```bash
python dupe_finder.py /path/to/folder
```

Each duplicate group is printed as a block of paths. Files are read in 1 MiB chunks; symlinks are skipped.

## Tests

```bash
python -m pytest -q
```

## License

MIT. See [LICENSE](LICENSE).
