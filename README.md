# TSPS

Time Series Photo Stock

1. find jpeg image from ``--from`` directory
2. copy jpeg image to ``--to`` directory
    - ``--to`` / ``YYYYmm`` / ``YYYYmmdd`` / ``YYYYmmdd_HHMMSS-MD5SUM.jpg``

Copy jpeg files from ``--from`` dir to ``--to`` dir.
At the time of copying, filename sets to ``YYYYmmdd_HHMMSS-MD5SUM.jpg`` and
saved to ``YYYYmm`` / ``YYYYmmdd`` .

ex: ``201506/20150623/20150623_130623-e3b0c44298fc1c14e3b0c44298fc1c14.jpg``

The time data get from EXIF date.
When EXIF's datetime cannot get, use original file timestamp.

# Usage

```
tsps --from /Volumes/NONAME --to ~/Pictures/mylife
```

May run with python 2.7, 3.7

# Install

```
pip install -r requirements.txt
```

