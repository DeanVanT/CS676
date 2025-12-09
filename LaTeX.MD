
# 1. LaTeX Expressions
- This is inline math: $E = mc^2$ in a sentence.
- Single $
---

- Here is a block equation:
- Double $$

$$
\int_{0}^{\infty} e^{-x^2} \, dx = \frac{\sqrt{\pi}}{2}
$$

---
# 2. Basics:
```
x^2                % superscript
x_1                % subscript
\frac{a}{b}        % fraction
\sqrt{x}           % square root
\sqrt[n]{x}        % n-th root

\alpha, \beta      % Greek letters
\sum_{i=1}^n i     % summation
\int_0^1 f(x)\,dx  % integral

a \le b, a \ge b   % ≤, ≥
a \neq b           % ≠
\infty             % ∞

\cdot, \times      % dot, ×
\pm, \mp           % ±, ∓

```
---
# 3. Matrices:

$$
\begin{bmatrix}
a & b \\
c & d
\end{bmatrix}
$$

---
# 4. Piecewise:

$$
f(x) = 
\begin{cases}
  x^2 & x \ge 0 \\
  -x  & x < 0
\end{cases}
$$

---