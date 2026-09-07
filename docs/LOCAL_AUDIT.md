# Audit of the local analytic argument

Audited source: the supplied Foregger manuscript, Sections 2–4, in [proof.pdf](../proof.pdf). Audit date: 8 September 2026.

## Conclusion

No mathematical gap was found in the local analytic argument. In particular, the stated radius implies every smallness condition, the derivative of the fixed power has the required leakage coefficient, and the recurrence for the non-averaged rows is valid without any commutation assumption. The local conclusion is

$$
\operatorname{per}(A)-\operatorname{per}(A^k)
\ge 4p\delta+\frac p8\|A-F\|_F^2
$$

for the manuscript's radius and every integer $k\ge16n^2$.

This is a separate AI-assisted analytical audit of the supplied argument, not formal proof-assistant verification or external peer review. It does not establish priority. The completed [global audit](GLOBAL_AUDIT.md) and [literature review](PRIORITY.md) cover the remaining portions.

## 1. Ambient contraction and row averaging

Every doubly stochastic matrix is a Euclidean contraction by Jensen's inequality followed by the column sums. Transposition gives the row-vector form. This applies to every power, independently of reducibility, periodicity, or any spectral gap.

For a row-averaged doubly stochastic matrix $M=EM$, let $y_{aj}=\sum_{i\in C_a}M_{ij}$. Each column of $y$ is a probability vector and $\sum_jy_{aj}=m_a$. Independently assigning column $j$ to class $a$ with this probability gives

$$
\frac{\operatorname{per}(M)}p
=\mathbb P(N_a=m_a\text{ for all }a),
\qquad
\mathbb E\|N-m\|_2^2
=n-\sum_{a,j}y_{aj}^2=V_E(M).
$$

The permanent identity has the correct factor: every successful class assignment contributes $\prod_a m_a!$ bijections, and every such bijection has product $\prod_j y_{a(j),j}/\prod_a m_a^{m_a}$.

Both $N$ and $m$ are nonnegative with coordinate sum $n$, hence $\|N-m\|_2^2\le2n^2$. Since the squared difference vanishes on the successful-assignment event, this proves the claimed occupancy bound. The constant is conservative but valid.

With $U$ having class-indicator rows,

$$
V_E(EA^k)=n-\|UA^k\|_F^2.
$$

Right multiplication by $A$ cannot increase the norm of any row, so this defect is nondecreasing. This monotonicity is the correct way to pass from one fixed power to arbitrarily late powers; no uniform mixing time is needed.

## 2. Orthogonal tangent/leakage split

In an allowed block of size $m$, the projection

$$
Y_{ij}=X_{ij}-r_i/m-c_j/m+t/m^2
$$

has zero row and column sums. Its complement is a sum of a row-constant and a column-constant matrix and is orthogonal to that tangent space. Outside the allowed blocks $Y=0$. Thus $X=Y+Z$ is orthogonal and

$$
\|X\|_F^2=\|Y\|_F^2+\|Z\|_F^2.
$$

All $r_i,c_j,t$ here are sums of $X$, not of $A$. Each $r_i,c_j$ is nonpositive, because the complete corresponding row or column of $X$ sums to zero, and the entries outside that allowed block are nonnegative. Therefore

$$
\sum_{\text{one block}}|Z_{ij}|
\le\sum_i|r_i|+\sum_j|c_j|+|t|=3(-t).
$$

The totals $-t$ sum to $\delta$. The outside entries of $Z$ are the outside entries of $A$, with total $\delta$. Hence $\|Z\|_F\le\|Z\|_1\le4\delta$.

The blockwise zero sums imply both $EY=0$ and $YE=0$ even when $F$ permutes the blocks. Orthogonal projection cannot increase the Frobenius norm, so every entry of $Y$ has absolute value at most $\varepsilon$. Since each allowed entry of $F$ is at least $1/n$, the condition $\varepsilon\le1/n$ ensures $F+Y\in\Omega_n$. The row and column sums are already correct.

## 3. Permanent derivatives and the starting value

For $n\ge2$, set $C=n^2(n-2)!/2$. On the Birkhoff polytope every second partial derivative is bounded in absolute value by $(n-2)!$. Consequently, for arbitrary ambient directions $H,K$,

$$
|D^2f(M)[H,K]|
\le(n-2)!\|H\|_1\|K\|_1
\le2C\|H\|_F\|K\|_F.
$$

Taylor's quadratic remainder is at most $C\|D\|_F^2$. For $n\ge3$, the cubic remainder along a segment in the polytope is at most

$$
\frac{n^3(n-3)!}{6}\|Y\|_F^3
\le C\|Y\|_F^3.
$$

The last comparison is $n/[3(n-2)]\le1$. For $n=2$ the third derivative is zero.

An allowed cofactor at $F$ is

$$
\frac{(m-1)!}{m^{m-1}}\prod_{b\ne a}\frac{m_b!}{m_b^{m_b}}=p.
$$

An outside cofactor is zero: deleting a row from one allowed block and a column from a different block leaves incompatible block matching counts. Since the total of $X$ on the allowed support is $-\delta$, the derivative is $Df_F(X)=Df_F(Z)=-p\delta$, while $Df_F(Y)=0$.

For a tangent block, inclusion–exclusion over equal rows and columns gives

$$
\sum_{i\ne h,\ j\ne\ell}Y_{ij}Y_{h\ell}=\|Y\|_F^2.
$$

The unordered row-pair factor $1/2$ and the complementary permanent give the coefficient $p\,m/[2(m-1)]$. The product over blocks introduces no quadratic cross terms because each block's linear term is zero. Thus the quadratic coefficient is at least $(p/2)\|Y\|_F^2$. If $C\varepsilon\le p/4$, subtracting the cubic remainder gives

$$
f(F+Y)\ge p+\frac p4\|Y\|_F^2.
$$

For $M_t=F+Y+tZ$, all points lie in the polytope and orthogonality gives $\|M_t-F\|_F\le\varepsilon$. Integrating the gradient difference along this segment gives an error at most $2C\varepsilon\|Z\|_F\le8C\varepsilon\delta$ when the linear term is evaluated at $F$. Therefore, if $8C\varepsilon\le p$ and $\delta\le1/4$,

$$
\begin{aligned}
f(A)&\ge p-2p\delta+\frac p4\|Y\|_F^2\\
&\ge p-2p\delta+\frac p4\varepsilon^2-4p\delta^2\\
&\ge p-3p\delta+\frac p4\varepsilon^2.
\end{aligned}
$$

The sign of the first derivative is important: leakage lowers the starting permanent to first order. The later-power estimate must and does have a larger linear decrease.

## 4. Derivative of a fixed power and defect growth

The exact noncommutative power derivative is

$$
D(A\mapsto A^r)_F[X]
=\sum_{j=0}^{r-1}F^jXF^{r-1-j}.
$$

For a precise support argument, write $S_r$ for the support of $F^r$. A class pair $(C_a,C_b)$ is allowed for $F$ exactly when $b=\pi(a)$. Under the term $F^jXF^\ell$, where $j+\ell=r-1$, it contributes to class pairs whose final column class equals $\pi^r$ of the initial row class exactly when the original pair was allowed. This is a bijection on the class-pair relations. Nonnegative doubly stochastic multiplication preserves the total mass of the outside part. Accordingly, each summand has outside mass $\delta$ relative to $S_r$ and inside total $-\delta$. This remains true when $j=0$ or $\ell=0$, so there is no endpoint exception.

Since $UF^r$ consists of deterministic class-indicator rows,

$$
\left\langle UF^r,\,
U\,D(A\mapsto A^r)_F[X]\right\rangle_F=-r\delta.
$$

Differentiating $g_r(A)=n-\|UA^r\|_F^2$ therefore gives exactly $Dg_r(F)[X]=2r\delta$.

Also $u_a^T(F+Y)=u_{\pi(a)}^T$, so iteration gives $U(F+Y)^r$ as the same deterministic class assignment. Thus $g_r(F+Y)=0$, and $Dg_r(F)[Y]=0$.

The operator-norm derivative bounds on the polytope are

$$
\|D(A^r)[H]\|_2\le r\|H\|_F,\qquad
\|D^2(A^r)[H,K]\|_2\le r(r-1)\|H\|_F\|K\|_F.
$$

There are respectively $r$ and $r(r-1)$ ordered placements of the differentiated factors; all remaining factors have operator norm at most one. Since $\|U\|_F^2=n$, the product rule gives

$$
|D^2g_r(A)[H,K]|
\le[2nr^2+2nr(r-1)]\|H\|_F\|K\|_F
\le4nr^2\|H\|_F\|K\|_F.
$$

Integrating from $F+Y$ to $A$, and comparing gradients to their values at $F$, now yields

$$
|g_r(A)-2r\delta|
\le4nr^2\varepsilon\|Z\|_F
\le16nr^2\varepsilon\delta.
$$

The condition $\varepsilon\le1/(16nr)$ makes the error at most $r\delta$. Monotonicity from Section 1 therefore gives $V_E(EA^k)\ge r\delta$ for **every** $k\ge r$. No Taylor expansion in the late exponent $k$ occurs.

## 5. The noncommuting recurrence

Define

$$
D_k=(I-E)A^k,\quad R=(I-E)AE,\quad T=(I-E)A(I-E).
$$

Because $(I-E)F=F(I-E)=0$ and $YE=0$,

$$
\|R\|_F\le4\delta,\quad \|T\|_2\le\varepsilon,\quad
\|D_1\|_F\le\varepsilon.
$$

The recurrence is exact in the stated order:

$$
\begin{aligned}
D_k&=(I-E)A(E+(I-E))A^{k-1}\\
&=RA^{k-1}+T D_{k-1}.
\end{aligned}
$$

The second equality uses $T(I-E)=T$, not commutation of $A$ with $E$ or $F$. Since $\|A^{k-1}\|_2\le1$, induction gives

$$
\|D_k\|_F
\le4\delta\sum_{j=0}^{k-2}\varepsilon^j+\varepsilon^k
\le8\delta+\varepsilon^k
$$

when $\varepsilon\le1/2$. For $k=1$ the sum is empty and the bound is still valid.

At $M=EA^k$, all cofactor rows within a class are equal because the matrix rows within that class are equal. The identity $ED_k=0$ means that the corresponding rows of $D_k$ sum to zero entrywise. Therefore $Df_M(D_k)=0$. Both endpoints $M$ and $M+D_k=A^k$ are doubly stochastic, so the permanent Hessian estimate gives

$$
f(A^k)\le f(EA^k)+C\|D_k\|_F^2.
$$

## 6. Radius and final constants

Take $r=16n^2$ and

$$
\rho_F=\min\left\{\frac1{16nr},\frac p{128Cn}\right\}.
$$

For $\varepsilon\le\rho_F$, the needed conditions follow as follows:

| Required condition | Reason |
| --- | --- |
| $\varepsilon\le1/n$ and $\varepsilon\le1/2$ | $\varepsilon\le1/(16nr)$, $n\ge2$, $r\ge1$ |
| $C\varepsilon\le p/4$ | $C\varepsilon\le p/(128n)$ |
| $8C\varepsilon\le p$ | $8C\varepsilon\le p/(16n)$ |
| $\delta\le1/4$ | $\delta\le n\varepsilon\le p/(128C)$; $p\le1$, $C\ge2$ |
| $128C\delta^2\le p\delta$ | $\delta\le p/(128C)$ |
| $2C\varepsilon^{2k}\le(p/8)\varepsilon^2$ | $\varepsilon\le1$, $2k-2\ge1$, $2C\varepsilon\le p/8$ |

The occupancy, fixed-time growth, and row-suppression estimates give

$$
\begin{aligned}
f(A^k)
&\le p-\frac{pr}{2n^2}\delta+C(8\delta+\varepsilon^k)^2\\
&\le p-8p\delta+128C\delta^2+2C\varepsilon^{2k}\\
&\le p-7p\delta+\frac p8\varepsilon^2.
\end{aligned}
$$

Subtracting this from the starting-matrix lower bound proves the claimed local gap. The $\varepsilon=0$ case holds directly; the estimate on $\varepsilon^{2k}$ does not require division by $\varepsilon$.

## 7. Boundary and equality checks

- If $F$ is a permutation, $E=I$ and $Y=0$. The row-suppression defect is identically zero, but the occupancy/mixing-defect argument remains valid.
- If $F=J_n$, there is no outside support, so $\delta=0$, $Y=X$, and $Z=0$. Then the argument reduces to a positive quadratic permanent gap against an exponentially suppressed tangent term.
- Nontrivial cycles of uniform blocks are covered because both the derivative support argument and the recurrence retain their original multiplication order.
- Blocks of size one have no nonzero tangent directions, so no factor $m/(m-1)$ is evaluated at $m=1$.
- For $n=2$ the cubic remainder vanishes and $C=2$; all stated constants remain valid.
- Within the stated neighborhood, the lower bound is strictly positive whenever $A\ne F$, because $p>0$ and $\varepsilon^2>0$. At $A=F$, every power has permanent $p$, including periodic $F$.

No repair to the manuscript's local argument was necessary. For exposition, the support-mass inner-product identity in Section 4 and the fully ordered recurrence in Section 5 make the two most delicate steps easier to inspect.
