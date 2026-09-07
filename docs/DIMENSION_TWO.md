# Exact exponent and sharp quadratic stability in dimension two

Every real nonnegative doubly stochastic $2\times2$ matrix is uniquely

$$
A(t)=\frac12
\begin{pmatrix}1+t&1-t\\1-t&1+t\end{pmatrix},
\qquad -1\le t\le1.
$$

Write $J=A(0)$ and $Q=I-J$. The identities $J^2=J$, $Q^2=Q$, and $JQ=QJ=0$ give

$$
A(t)=J+tQ,\qquad A(t)^k=J+t^kQ=A(t^k).
$$

Direct expansion gives

$$
\operatorname{per}(A(t))=\frac{1+t^2}{2},
\qquad
\operatorname{per}(A(t))-\operatorname{per}(A(t)^k)
=\frac{t^2-t^{2k}}2.
$$

For every integer $k\ge2$, this is nonnegative, and equality holds precisely for $t\in\{-1,0,1\}$. These three matrices are exactly $\mathcal F_2$: the two permutations and $J_2$. Thus the smallest nontrivial threshold, under the requirement $N(2)\ge2$, is $N(2)=2$. The inequality alone also holds at $k=1$; the stated equality classification requires $k\ge2$.

Moreover, $\|A(t)-A(u)\|_F=|t-u|$. Setting $s=|t|\in[0,1]$ gives

$$
\operatorname{dist}_F(A(t),\mathcal F_2)=\min\{s,1-s\}.
$$

Since $k\ge2$,

$$
\frac{s^2-s^{2k}}2\ge\frac{s^2(1-s^2)}2.
$$

If $s\le1/2$, then

$$
4s^2(1-s^2)-3s^2=s^2(1-2s)(1+2s)\ge0.
$$

If $s\ge1/2$, then

$$
4s^2(1-s^2)-3(1-s)^2
=(1-s)(2s-1)(2s^2+3s+3)\ge0.
$$

Consequently the explicit stability inequality is

$$
\boxed{
\operatorname{per}(A)-\operatorname{per}(A^k)
\ge\frac38\,\operatorname{dist}_F(A,\mathcal F_2)^2
\qquad(k\ge2).
}
$$

The constant $3/8$ is optimal when the inequality is required for every $k\ge2$: at $t=1/2$ and $k=2$, the permanent gap is $3/32$ and the squared distance is $1/4$, giving ratio $3/8$.

This is a self-contained calculation and a sharper explicit dimension-two consequence than the conservative general local bound. It makes no priority claim.
