# Foregger per-k conjecture: historical and priority review

Review date: 8 September 2026. Sources below were read directly during this review. This is a bounded search, not a guarantee of first discovery or a comprehensive external literature review.

## Assessment

The proposed theorem addresses a real, precisely identified historical conjecture. Its dimension-only threshold removes the entry-bound dependence present in the closest inspected general result, and its assertion for **every** sufficiently large exponent is stronger than the catalogue's request for one common exponent. The equality and quantitative stability assertions are additional claims.

No earlier publication of the same unrestricted uniform theorem was located. That finding is not proof that no such work exists. Subject to mathematical correctness and priority, this would be a meaningful result on matrix permanents. It is reasonable to publish a clearly labelled candidate manuscript and reproducibility repository, but not to claim certified first priority, peer review, or a complete machine-checked proof.

Compared with the Cameron note, this candidate has a stronger documented history of unsuccessful partial progress on the exact uniform question. That supports taking it seriously as potentially more significant; editorial importance cannot be determined by age alone. The global argument survived this review, conditional on the separate local-lemma audit.

## The exact historical target

[Cheon–Wanless, *An update on Minc's survey of open problems involving permanents* (2005), p. 326, Conjecture 17](https://users.monash.edu.au/~iwanless/papers/permsurveyLAA.pdf) asks whether, for each dimension `n`, a common integer exponent `k(n)` satisfies `per(A^k(n)) <= per(A)` for all doubly stochastic `A`. It attributes the conjecture to Foregger in Minc's 1978 book; reference [68] confirms that bibliographic identification. It records Chang's dimension-three result and a partial theorem for matrices with permanent at least one half. The catalogue's displayed wording does not explicitly exclude `k=1`; the nontrivial interpretation is made explicit by the thesis below.

[Melnykova, *Notes on Foregger's Conjecture* (2012)](https://mspace.lib.umanitoba.ca/bitstreams/fb4ed590-ea0c-4117-86ce-0eb806ae8427/download), printed pp. 38–42 (PDF pp. 41–45): Conjecture 4.1 requires `k(n)>1`, independent of `A`. The author reports Foregger's direct account of a letter to Minc dated 17 December 1977; this review did not inspect that letter or the original book page. Theorem 4.3 attributes exponent eight for `n=3` to Chang. Theorem 4.10 proves an eventual threshold depending on both `n` and a fixed lower bound `c>0` for the nonzero entries. Corollary 4.11 gives a matrix-dependent exponent for each individual matrix. Both statements were checked in the downloaded primary thesis, rather than inferred from a search snippet. The copyright page confirms 2012.

[Zhang, *An update on a few permanent conjectures* (2016), p. 313](https://scholars.nova.edu/ws/portalfiles/portal/42826589/An%20Update%20on%20a%20Few%20Permanent%20Conjectures.pdf) explicitly calls this the Foregger per-k conjecture, dates it to 1978, and cites Minc p. 157. It reports Chang's partial results. This is another historical source, not contemporary proof of open status.

## Later firsthand status evidence

[Ian Wanless's MathOverflow answer, 15 May 2022](https://mathoverflow.net/questions/422029/on-permanent-of-a-square-of-a-doubly-stochastic-matrix/422581) identifies the common-exponent question as Conjecture 17 and states that, to his knowledge then, it remained open. This is a dated first-person mathematical statement, not a journal article or an exhaustive 2026 status check.

The [same discussion](https://mathoverflow.net/questions/422029/on-permanent-of-a-square-of-a-doubly-stochastic-matrix) contains Joseph Van Name's answer dated 8 May 2022 with the four-by-four example having permanent `1/8` and square permanent `9/64`. That example rules out exponent two in general; it does not refute eventual decrease. Attribution to Van Name is correct, but “publicly posted example” is clearer than “published example” when describing its publication status.

## Distinguishing similarly named problems

[Lavi, *A counterexample to the Foregger–Sinkhorn tie-point conjecture*, arXiv:2608.13025v1, 13 August 2026](https://arxiv.org/html/2608.13025v1) addresses a condition connecting a zero's permanental cofactor to the support's tie-point property. The introduction identifies it as catalogue Conjecture 41, and the paper gives an order-eight counterexample. This is a different statement from Conjecture 17 and does not settle the matrix-powers question.

[*The Inequalities of Merris and Foregger for Permanents* (2021)](https://www.mdpi.com/2073-8994/13/10/1782) concerns, among other topics, the permanent of mixtures `tJ+(1-t)A`. Its use of Foregger's name should not be counted as a resolution of the ordinary-powers conjecture. Similarly, [*Lih Wang's and Dittert's conjectures on permanents* (2024)](https://www.degruyterbrill.com/document/doi/10.1515/spma-2024-0006) addresses related mixture/optimization inequalities rather than this target.

## Search and access limits

Queries combined Foregger, per-k, permanent, powers, ordinary powers, uniform exponent, `k(n)`, eventual, solved, proof, and years 2024–2026. Results were compared against the actual statements above. Neither broad searches nor quoted-name searches located a previous unrestricted uniform theorem. That coverage omits unindexed manuscripts, private communication, paywalled reviews not accessed here, and possible concurrent work. No author or expert was contacted.

Chang's 1984 publisher abstract was accessible at [DOI 10.1080/03081088408817602](https://www.tandfonline.com/doi/abs/10.1080/03081088408817602), but the full original 1984 and 1990 papers were not independently inspected. Their detailed results are attributed through the identified later sources. The original 1978 book page and 1977 letter likewise remain uninspected. The thesis download succeeded despite unreliable browser extraction; the relevant theorem and corollary were verified locally from its text.

The supplied reproducibility ZIP is available and was extracted. Its `sources/prior_art.md` and `sources/query_log.txt` were compared with this review: their target, chronology, closest prior theorem, distinct-conjecture exclusions, and cautious priority boundaries agree with the independently inspected sources. Their reported search history is supplied provenance, not an independent execution log for this review.

Suggested public status: **“Candidate proof of Foregger's 1978 permanent-of-powers conjecture, with eventual equality and stability claims. The analytic argument and exact diagnostics are supplied for independent review; priority is not certified.”**
