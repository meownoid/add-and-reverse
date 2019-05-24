## Usage
```bash
cythonize -ai _fast.pyx
python main.py --threads 8 --numbers 10000 --chunk-size 1000
```

You should see something like this:
```bash
Start: 1
End: 10000
Number of processes: 8
Found new numbers: 21
```

Now the first 21 found numbers are stored in the `db.sqlite`.