# SyncDirectories
A fast tool to synchronize directories file by file.

Usage:
```
$ python syncDirectories.py -s <source_directory> -d <destination_directory>
```

Options:
 * -s, --srcdir <dir>:    source directory used as reference for synchronization
 * -d, --dstdir <dir>:    destination directory to synchronize
 * -c, --checkdiff:       check precise files difference (slower)
 * -t, --test:            test synchronization simulation (traces only, no effects)
 * -h, --help:            display help
