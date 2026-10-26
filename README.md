# Mathematical Computing: Pell's Equation

## Problem Statement

Find the nonsquare integer $D$ in the range $2 \le D \le 10000$ whose fundamental Pell solution has the largest value of $x$.

For every nonsquare integer $D$ in this range, find the minimal positive integer solution $(x,y)$ to Pell's equation:

$$
x^2 - Dy^2 = 1
$$

Then determine:

**Which value of $D \le 10000$ produces the largest minimal $x$?**

### Why Not Brute Force?

A straightforward approach would be to test successive positive integers for $y$ until we find a value for which $Dy^2+1$ is a perfect square.

For each candidate $y$, we would calculate:

$$
x = \sqrt{Dy^2+1}
$$

If $x$ is an integer, we have found a solution.

However, this approach becomes impractical because the fundamental solutions can be extremely large.

Consider a few examples:

| $D$ | Minimal $y$ | Fundamental $x$ |
|---:|---:|---:|
| 2 | 2 | 3 |
| 3 | 1 | 2 |
| 5 | 4 | 9 |
| 13 | 180 | 649 |
| 61 | 226,153,980 | 1,766,319,049 |

For $D=61$, a brute-force approach would need to examine more than 226 million candidate values of $y$ before finding the minimal solution.

For larger values of $D$, the minimal solutions can contain many digits, making brute force unsuitable for searching the entire range.

We therefore need a mathematical method that finds the fundamental solution efficiently.

---

## Mathematical Solution

We use **continued fractions** to find the fundamental solution of Pell's equation.

### 1. Understanding the Relationship Between $x/y$ and $\sqrt{D}$

Starting with Pell's equation:

$$
x^2 - Dy^2 = 1
$$

Rearrange it:

$$
x^2 = Dy^2 + 1
$$

Divide both sides by $y^2$:

$$
\frac{x^2}{y^2} = D + \frac{1}{y^2}
$$

Taking the square root gives:

$$
\frac{x}{y} = \sqrt{D + \frac{1}{y^2}}
$$

Since $D$ and $y$ are positive:

$$
\frac{x}{y} > \sqrt{D}
$$

When $y$ is large, $\frac{1}{y^2}$ becomes very small. Therefore, $\frac{x}{y}$ is a rational number that lies very close to $\sqrt{D}$, just above it.

Continued fractions provide particularly good rational approximations to irrational numbers. Their convergents help us find the fundamental solution of Pell's equation.

### 2. Generate the Continued Fraction of $\sqrt{D}$

For every positive nonsquare integer $D$, the continued fraction expansion of $\sqrt{D}$ is periodic.

For example:

$$
\sqrt{5} = [2;\overline{4}]
$$

This notation means:

$$
\sqrt{5} = [2;4,4,4,\ldots]
$$

The continued fraction consists of:
- An initial integer part, $a_0$.
- A repeating sequence of coefficients called the period.

For $\sqrt{5}$:

$$
a_0 = 2
$$

The repeating period is:

$$
[4]
$$

Its period length is therefore:

$$
L = 1
$$

Our implementation generates these coefficients using integer arithmetic rather than floating-point approximations.

### 3. Generate the Convergents

A **convergent** is a rational approximation obtained by truncating a continued fraction.

For $\sqrt{5}$, the first two convergents are:

$$
\frac{2}{1}, \qquad \frac{9}{4}
$$

The first convergent is:

$$
\frac{x}{y} = \frac{2}{1}
$$

Substituting $x=2$, $y=1$, and $D=5$ into Pell's equation gives:

$$
2^2 - 5(1^2) = -1
$$

This does not satisfy the required equation:

$$
x^2 - Dy^2 = 1
$$

The next convergent is:

$$
\frac{x}{y} = \frac{9}{4}
$$

This gives us a candidate solution:

$$
x=9,\qquad y=4
$$

### 4. Determine the Fundamental Solution

We can verify the candidate by substituting it into Pell's equation:

$$
x^2 - Dy^2 = 1
$$

For $D=5$, $x=9$, and $y=4$:

$$
9^2 - 5(4^2) = 81 - 80 = 1
$$

Therefore, the fundamental solution is:

$$
\boxed{(x,y)=(9,4)}
$$

However, testing convergents one by one is not the most efficient strategy. We can use the period length of the continued fraction to determine which convergent produces the fundamental solution.

Let $L$ be the length of the repeating period of the continued fraction of $\sqrt{D}$.

- If $L$ is even, the fundamental solution is the convergent at index $L-1$.
- If $L$ is odd, the fundamental solution is the convergent at index $2L-1$.

The indexing starts at $0$, with the integer part $a_0$ at index $0$.

For $D=5$, the period length is $L=1$, which is odd. Therefore, we use the convergent at index:

$$
2L-1 = 2(1)-1 = 1
$$

The convergent at index $1$ is $\frac{9}{4}$, giving the fundamental solution $(9,4)$.

This property lets us calculate the required convergent directly rather than searching indefinitely.

---

## Algorithm and Implementation

The solution is divided into four main functions.

### 1. `continued_fractions(D)`

Generates the continued fraction coefficients of $\sqrt{D}$.

The implementation uses integer arithmetic to calculate the coefficients accurately, avoiding potential floating-point precision issues.

For example:

```python
continued_fractions(5)
```

Output:

```python
[2, 4]
```

The first element is the integer part $a_0=2$, and the remaining elements contain one copy of the repeating period.

### 2. `convergents(coefficients)`

Generates the convergents from a sequence of continued fraction coefficients.

The numerator and denominator are calculated recursively:

$$
p_n = a_n p_{n-1} + p_{n-2}
$$

$$
q_n = a_n q_{n-1} + q_{n-2}
$$

Here:
- $a_n$ is the current continued fraction coefficient.
- $p_n$ is the numerator of the current convergent.
- $q_n$ is the denominator of the current convergent.

The initial values are:

$$
p_{-2}=0,\qquad p_{-1}=1
$$

$$
q_{-2}=1,\qquad q_{-1}=0
$$

These recurrence relations allow us to generate convergents efficiently without repeatedly evaluating the entire continued fraction.

### 3. `pells_solver(D)`

Finds the fundamental solution $(x,y)$ for a given nonsquare integer $D$.

The function:

1. Validates the input.
2. Rejects perfect squares, for which the algorithm is not applicable.
3. Generates the continued fraction coefficients.
4. Determines how many coefficients are required based on the period length.
5. Generates the necessary convergents.
6. Returns the fundamental solution $(x,y)$.

### 4. `find_largest_minimal_x(limit)`

Searches all nonsquare integers in the range $2 \le D \le \text{limit}$.

For each candidate $D$, the function:

1. Skips perfect squares.
2. Calculates the fundamental solution using `pells_solver(D)`.
3. Compares the resulting $x$ with the largest value found so far.
4. Updates the best $D$, $x$, and corresponding $y$ when a larger $x$ is found.

Finally, it returns the value of $D$ that produces the largest minimal $x$, along with the corresponding $x$ and $y$.

---

## Results

Running the algorithm for all nonsquare integers in the range:

$$
2 \le D \le 10000
$$

produces the following result.

**Value of $D$ with the largest minimal $x$:**

$$
\boxed{D=9949}
$$

The corresponding fundamental solution is:

$$
x =
23551019614858223475933893515741198183163217312913587552899320396564478041197360918469501097146448985821854465768234479384482435117587576296319428592757548743265811454938493105633433315887574461850060798834186249
$$

$$
y =
236113054062810988826514929828649213339688520849720684015415366388626019230322623673232286474879711003505448178417385617250641629212134427833135509077013929303770208680820795381507114806491325360400076633910900
$$

These values satisfy Pell's equation:

$$
x^2 - 9949y^2 = 1
$$

The equation is verified using Python's arbitrary-precision integers, which can handle the very large values of $x$ and $y$ without integer overflow.

Execution Time

The complete search over the range $2 \le D \le 10000$ took approximately 0.114 seconds in a local benchmark.

Actual execution time depends on the hardware and Python environment.

Testing

The project includes a test suite using pytest.

The tests cover:

Known fundamental solutions for $D=2,3,5,13,61$.

Verification that the calculated solutions satisfy Pell's equation.

Input validation for invalid values of $D$.

Rejection of perfect-square values.

Input validation for the search function.

Verification of the final result for the range up to $D=10000$.

Run the tests from the project root:

`pytest -v`

All 20 tests pass.

Example Usage

To find the fundamental solution for $D=61$:

```
from solver import pells_solver

x, y = pells_solver(61)

print(f"x = {x}")
print(f"y = {y}")
print(x * x - 61 * y * y)
```
The final statement should print:

1

To find the value of $D$ that produces the largest minimal $x$ up to $10000$:

```
from solver import find_largest_minimal_x

D, x, y = find_largest_minimal_x(10000)

print(f"D = {D}")
print(f"x = {x}")
print(f"y = {y}")
```
Project Structure

```
mathematical-computing/

├── solver.py
├── run_solver.py
├── tests/
│   └── test_solver.py
├── README.md
└── requirements.txt
```
requirements.txt can contain the development dependency:

`pytest`

The solver itself uses Python's standard library, including math.isqrt, and does not require third-party mathematical libraries.

## Complexity Analysis

Let $N$ be the upper limit of the search, and let $L_D$ be the continued fraction period length for a particular nonsquare $D$.

The algorithm examines each integer from $2$ through $N$, skipping perfect squares.

For each nonsquare candidate, the solver generates the continued fraction coefficients and calculates the required convergent.

The number of recurrence steps for a given $D$ is proportional to its period length, with at most approximately $2L_D$ coefficients required.

Therefore, the search performs approximately:

$$
O\left(\sum_{\substack{2 \le D \le N\D\text{ nonsquare}}} L_D\right)
$$

arithmetic recurrence steps, ignoring the cost of operating on increasingly large integers.

Important: This expression describes the number of recurrence steps, not the complete bit-level runtime. Since $x$ and $y$ can become very large, the cost of arbitrary-precision integer arithmetic also affects execution time.

The continued-fraction approach avoids the impractical search through successive values of $y$ required by brute force.

## Key Takeaway

This project demonstrates how a mathematical insight can transform a computationally impractical problem into an efficient algorithm.

Instead of testing millions or billions of possible values of $y$, the solution uses:

Periodic continued fractions to represent $\sqrt{D}$.

Convergents to obtain rational approximations.

Period length properties to identify the fundamental solution.

Integer arithmetic to maintain numerical accuracy.

Automated tests to verify correctness.

The final search identifies $D=9949$ as the value that produces the largest minimal $x$ for nonsquare integers in the range $2 \le D \le 10000$.