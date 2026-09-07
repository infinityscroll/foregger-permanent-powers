# Validation repairs and preserved results

The supplied ZIP remains unchanged in archive/original-package.zip. Its embedded manifest contains 25 files. The original package and the repaired working copies each regenerated both fixture files and all seven mathematical output files byte for byte.

Two weaknesses affected malformed-input handling and coverage checks, rather than the diagnostic arithmetic:

1. The C++ parser indexed the class-size vector using a class image before validating every image. An input such as pi=[100,0] could read out of bounds. Failed header extraction could also leave indeterminate integers in use. The working parser checks extraction before dependent use, validates bounded sizes and every class image, verifies the entire permutation, and only then checks preservation of block sizes.
2. The local-power audit required only a total of 42 accepted rows. Repeating one valid late-power record 42 times could therefore conceal missing fixtures. The working audit requires unique fixture IDs and exactly the two intended exponents, $16n^2$ and $16n^2+1$, for each selected fixture. It rejects duplicates, missing keys, and unexpected late exponents.

The repaired files are src/audit_cpp.cpp and src/audit_local.py. Their arithmetic and reference results are unchanged. The original 17-guard report is retained for reproducibility.

The additional tests/hardening_regressions.py suite has 15 regressions: 11 C++ malformed-input cases and four local-record coverage cases. C++ rejection must use the ordinary validation exit code and diagnostic; a crash does not count as successful rejection. These tests passed with both the ordinary repaired binary and address/undefined-behavior sanitizers during the review.

After compiling the diagnostic binary, run:

    python3 tests/hardening_regressions.py --cpp build/reproduced/build/audit_cpp --output build/hardening_regressions.json

The original comparison's 4,500 numeric fields include 1,080 IDs and 900 exponents, leaving 2,520 mathematical output values across 1,080 records. The README and verification guide make that distinction explicit.

The original README, manifest, PDF, LaTeX source, and archive remain available as supplied provenance. The working manifest covers the repaired sources and added material. Neither manifest certifies mathematical correctness or authorship.

See ORIGINAL_CODE_AUDIT.md for the defect reproductions and mathematical scope of the original implementations.
