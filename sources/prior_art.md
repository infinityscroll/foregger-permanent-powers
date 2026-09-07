# Target, prior-art, and significance audit

**Search and inspection date:** 7 September 2026 (UTC).  
**Claim under review:** a common eventual threshold for permanent comparison on the entire fixed-dimensional Birkhoff polytope; strictness/equality classification; uniform quadratic stability.

## Exact target and chronology

Foregger's permanent-of-powers conjecture asks: for every positive integer n, does there exist **k(n)>1**, independent of the doubly stochastic matrix A, such that per(A^k(n)) <= per(A)? Ordinary matrix powers are meant. The claim in this package proves the stronger all-k-beyond-a-threshold statement. It does not use the trivial exponent one.

The 2005 Cheon–Wanless primary survey prints the target as Conjecture 17 on page 326, referring to Minc's 1978 book. Melnykova's 2012 thesis explicitly supplies k>1 and reports that Foregger told her he stated it in a letter to Minc on 17 December 1977. The original letter and original book page were not inspected. Publication in 1978 suffices for the requested age criterion.

## Inspected primary sources

**S1. Cheon and Wanless (2005).** Gi-Sang Cheon and Ian M. Wanless, *An update on Minc's survey of open problems involving permanents*, Linear Algebra and its Applications 403, 314–342. DOI: 10.1016/j.laa.2005.02.030. Author-hosted PDF: https://users.monash.edu.au/~iwanless/papers/permsurveyLAA.pdf . The introduction, Conjecture 17, and relevant references were inspected. The conjecture page was rendered and visually checked. This is objective evidence of the target's place in the permanent-theory open-problem catalogue, not evidence that every conjecture in it has equal importance.

**S2. Melnykova (2012).** Kateryna Melnykova, *Notes on Foregger's Conjecture*, M.Sc. thesis, University of Manitoba. Official PDF: https://mspace.lib.umanitoba.ca/server/api/core/bitstreams/fb4ed590-ea0c-4117-86ce-0eb806ae8427/content . Title/year, exact conjecture, history, Chapter 4 partial results and proof methods were inspected. Printed pages 38 and 41 were visually checked. Theorem 4.10 has a threshold depending on n and a lower bound c on nonzero entries; Corollary 4.11 gives a matrix-dependent exponent. Neither is the unrestricted uniform statement proved here. These existing results and their priority are preserved.

**S3. Zhang (2016).** Fuzhen Zhang, *An update on a few permanent conjectures*, Special Matrices 4, 305–316, DOI: 10.1515/spma-2016-0030. https://arxiv.org/html/1608.02844v1 . The Foregger per-k paragraph, related conjecture distinctions, and bibliography were inspected. This survey states the target as conjectural and records Chang's partial results. Its 2016 status report is not represented as an exhaustive 2026 search. It omits the explicit restriction k>1 in the wording, which is recovered from S2 rather than exploited.

**S4. Chang (1990), metadata and attributed results.** Derek K. Chang, *On two permanental conjectures*, Linear and Multilinear Algebra 26, 207–213; DOI: 10.1080/03081089008817977. Publisher metadata: https://www.tandfonline.com/doi/abs/10.1080/03081089008817977 . The n=3 proof (exponent eight) and other partial results are attributed through S1–S3. The full original paper was not independently read. The earlier 1984 paper, *A note on a conjecture of T. H. Foregger*, was identified in those references; an attempted publisher fetch did not provide its full text. Repository upload dates were not mistaken for publication dates.

**S5. Gurvits, classical imported theorem.** Leonid Gurvits, *Van der Waerden/Schrijver–Valiant like conjectures and stable (aka hyperbolic) homogeneous polynomials: one theorem for all*, https://arxiv.org/html/0711.3496v2 . The introduction explicitly states per(A) >= n!/n^n with unique equality at J_n and attributes the lower bound to Falikman and the full equality statement to Egorychev. The source supplies an independent polynomial treatment. The present work does not claim the van der Waerden theorem, its equality classification, or the standard Markov cyclic decomposition as new.

**S6. Lavi (2026), excluded as a different target.** Yair Lavi, *A counterexample to the Foregger–Sinkhorn tie-point conjecture*, 13 August 2026, https://arxiv.org/html/2608.13025v1 . This concerns a prescribed zero, a permanental cofactor, and a face minimizer, not matrix powers. Its already-public counterexample is not a discovery in this package and does not by itself answer the per-k target.

**S7. Udayan and Somasundaram (2021), excluded as a different inequality.** *The Inequalities of Merris and Foregger for Permanents*, Symmetry 13(10), 1782; https://www.mdpi.com/2073-8994/13/10/1782 . The indexed abstract describes a Foregger expression involving t J_n + (1-t)A rather than A^k. The official issue listing confirmed the publication metadata, but the article-page fetch failed; the full article was not inspected. This is an exclusion of a differently worded target, not a claim to have audited that whole paper.

**S8. Van Name and Wanless (2022), dated original author discussion.** Joseph Van Name's answer of 8 May 2022 and Ian M. Wanless's answer of 15 May 2022 to *On permanent of a square of a doubly stochastic matrix*, MathOverflow question 422029: https://mathoverflow.net/questions/422029/on-permanent-of-a-square-of-a-doubly-stochastic-matrix . The complete relevant answers were inspected. Van Name gives the 4-by-4 counterexample to the stronger k=2 assertion; it is explicitly credited and independently recomputed in `src/calibration.py`. Wanless identifies Foregger's Conjecture 17 and says that, as far as he knows, it remains open. This is a primary dated statement by a survey coauthor, but it is not peer-reviewed publication, exhaustive bibliography, or evidence of no development after May 2022.

## Novelty boundaries

The proposed new result is the **uniform theorem on all of Omega_n**, together with its strict equality classification and quadratic stability consequence. The classical lower bound, Markov-chain convergence, permanent matching interpretation, elementary Taylor formulas, and stochastic contraction are known ingredients. The categorical counting identity and its use here are proved explicitly; no independent priority claim for that identity in isolation is made.

The search covered exact-name variants, the catalogue number, matrix-power wording, the author's thesis, uniform/eventual formulations, current-year work, and distinctive proof-mechanism terms. It found no earlier publication of the specific uniform theorem or the local gap proved here. The available search engines are incomplete, and some original articles were accessible only through metadata and later primary accounts. No authors were contacted; no private manuscripts, subscription-only full citation database, or unindexed work was searched.

**Defensible conclusion:** apparently unpublished in the inspected and indexed sources as of the dated search. Worldwide novelty and current priority are **not certified**. The 2012 thesis must not be omitted from any submission; it is the closest inspected prior work.

## Adversarial significance review

The result is more than a finite check or a small counterexample to a side assertion. Its exact quantifiers resolve a catalogue conjecture from 1978 across every matrix dimension, remove an essential lower-entry restriction from the closest inspected theorem, identify all eventual equality cases, and yield a uniform quadratic gap. Those are substantive advances in permanent inequalities and stochastic matrix theory, assuming the proof survives independent review.

The strongest limitations are that the global threshold is nonexplicit, the new method uses elementary/classical ingredients rather than a demonstrated new computational algorithm, and no direct engineering, quantum-computing, or complexity-theoretic speedup follows. The broad importance of permanents cannot be borrowed to imply an application not proved. A specialist journal-level contribution appears credible; a top-tier editorial verdict or broad science-news outcome is not certified by this self-review.

**External review status:** none. The mathematical and implementation audits were performed in this assistant session. They are not independent peer review or a formal proof-assistant check.
