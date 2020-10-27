# Most delayed palindromes generator

This is an utility that I used to solve little programming quiz back at the university.

## Problem statement

We asked to find the most delayed palindrome for any natural number.

Most delayed palindrome of N is a **smallest** decimal natural number which in **exactly** N iterations of
the reverse-and-add operation results in the palindrome in the duodecimal system (and at none
of the previous iterations it is a palindrome).

Palindrome is the number that satisfies `str(n) == ''.join(reversed(str(n)))` (assuming str works
in duodecimal system).

Reverse-and-add operation can be defined as `lambda n: n + int(reversed(str(n)))` (assuming str works
in duodecimal system).

### Example

Let's see an example of number 23 (decimal) = 1B (duodecimal).

First iteration:

1B + 1B = 110 (duodecimal)

Second iteration:

110 + 110 = 121 (duodecimal)

121 (duodecimal) is a palindrome which makes 23 (decimal) second 
most delayed palindrome. The first one is 12 and the zeroth one is 1.

## Solution

Let's just iterate over all natural numbers from 1 to infinity, applying to them
add-and-reverse operation iteratively, M iterations maximum. At some point we will
find all first M most delayed palindromes.

The key is efficiency. My implementation is written in Cython and is paralleled using multiprocessing.
It achieves the performance of `14277` numbers per second per thread
on the Intel Core i5 1.4 Ghz (with 200 iterations per number).

## Usage

Clone the repository.

```shell script
git clone https://github.com/meownoid/add-and-reverse.git
cd add_and_reverse
```

Install dependencies.

```shell script
pip install -r requirements.txt
cythonize -ai _fast.pyx
```

Build Cython code.

```shell script
cythonize -ai _fast.pyx
```

After that you should be able to start computation.

```shell script
python main.py --threads 8 --numbers 10000
```

Output should look like following.

```
Start: 1
End: 80000
Number of threads: 8
Found new numbers: 45
Bye
```

Now the first 45 found numbers are stored in the `db.sqlite`.
Starting the program next time will restore last saved state and computation will continue.

To print results and exit use the `--results` argument.

```shell script
python main.py --results
```

To benchmark performance while computing use the `--benchmark` argument.

```shell script
python main.py --benchmark
```

Benchmark results will be printed after the computation.

```
Benchmark results:
    Total time: 8.755 seconds
    Numbers per second: 114223
    Numbers per second per thread: 14277
```

To run tests use `pytest`.

```shell script
pip install pytest
pytest test.py
```

## Results (up to 100)

| n | result |
|---|--------|
0|1
1|12
2|23
3|83
4|95
5|236
6|107
7|248
8|267
9|1139
10|1847
11|2445
12|1547
13|273
14|131
15|21996
16|1835
17|274
18|280
19|1535
20|22404
21|22275
22|21655
23|21645
24|22048
25|21862
26|3587
27|3449
28|39736
29|40607
30|41471
31|43187
32|21921
33|21726
34|21754
35|22162
36|30524
37|15647
38|229079
39|22090
40|26632
41|62987
42|29806
43|333210
44|146123
45|22148
46|30951
47|267704
48|271143
49|83195
50|29514
51|2996385
52|3003944
53|3004326
54|3741686
55|2997888
56|3006611
57|3006407
58|3087848
59|3108534
60|3250214
61|4745796
62|4230573
63|3002068
64|5482792
65|3002589
66|3006222
67|4230137
68|3055027
69|3003385
70|3000658
71|3735496
72|4996357
73|3058524
74|53766429
75|29867135
76|5478765
77|3006523
78|3000199
79|996191
80|255738
81|145931
82|143855
83|353940
84|430124574
85|430121283
86|431991805
87|430114053
88|430140883
89|430561503
90|430115012
91|430197084
92|179169803
93|36038359
94|23906759
95|286673255
96|46158332
97|27117431
98|503428020
99|7453043706
100|3009901223
