# Most delayed palindromes generator

This is a program that I used to solve little quiz back in the university.

## Problem statement

## Solution

## Usage
I recommend building this program in-place.

```bash
pip install -r requirements.txt
cythonize -ai _fast.pyx
```

After that you should be able to start computation:
```bash
python main.py --threads 8 --numbers 10000
```

You should see something like this:
```bash
Start: 1
End: 80000
Number of processes: 8
Found new numbers: 45
```

Now the first 45 found numbers are stored in the `db.sqlite`.
