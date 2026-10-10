# Data dictionary

## Unit names

| File index | Audit unit | Passage | Aligned blocks |
| --- | --- | --- | ---: |
| 1 | Verse | Chapter 2 vv. 1–145 | 300 |
| 2 | Prose | Chapter 2 prose | 159 |
| 3 | Whole | Whole Chapter 2 | 459 |
| 4 | G1 | vv. 1–7 | 14 |
| 5 | G2 | vv. 8–21 | 28 |
| 6 | G3 | vv. 22–29 | 16 |
| 7 | G4 | vv. 30–37 | 16 |
| 8 | G5 | vv. 38–41 | 8 |
| 9 | G6 | vv. 42–145 | 218 |
| 10 | Pr1 | KN 29.1–30.8 | 22 |
| 11 | Pr2 | KN 33.5–38.1 | 34 |
| 12 | Pr3 | KN 38.8–59.7 | 103 |

The source file labels `(P1)`, `(P2)`, `(P3)` denote prose units, written Pr1–Pr3 in
the audit to distinguish them from the manuscript sigla P1–P3.

## Witnesses and transcriptions

Each aligned block has a KN reference row and 33 manuscript rows: 27 Nepalese
witnesses (K, Pk, C1–C6, B, R, P1–P3, T2–T9, A1–A3, N1–N3), D1–D3 (Gilgit),
O (Kashgar), F and M. KN is an edition/reference row, not a manuscript.
TAB characters separate alignment fields; physical LF lines define rows.
`<LAC>` marks physical loss. Editorial references, blank fields and unequal field
counts must be handled explicitly rather than silently treating all fields as text.

## Original matrix exports

`correlation_matrix-...csv` is a square matrix with KN plus 33 manuscript labels,
containing symmetric edit similarities from 0 to 1. It is not a statistical
correlation matrix. `similarity_matrix-...csv` is a percentage-formatted partner
ranking table. Numeric values agree with the square matrices at display precision,
but 22 adjacent ordering inversions occur because the observed lists follow string order.
Do not infer numeric rank from the order of those original lists.

## Audit outputs

`pair_checks.csv` has 12 × 528 = 6,336 manuscript-pair rows, excluding KN.
`export_pct` is the original matrix value × 100. `legacy_*` counts original font
symbols, while `unicode_*` counts supplied Unicode code points without extra NFC
normalization. `*_difference_pp` is recalculated minus exported percentage points.
`*_matches` uses an absolute tolerance below 1e-8 percentage points.
Coverage columns record retained blocks, retained fields, one-sided or two-sided
empty fields, and blocks flagged for unequal field counts.

In `unit_summary.csv`, `all` means 33 witnesses / 528 pairs; `without_F` means
32 / 496; and `without_F_M` means 31 / 465. Only positive exported cells count in
the `positive_match` columns. Agreement on unavailable zero cells is not a
reproduced measurement.

`strict` excludes the pair's entire block if field counts differ. `zip_diagnostic`
discards unmatched trailing fields as a diagnostic. `both_blank_counted` counts
two cleaned blank fields as agreement. The latter two are sensitivity diagnostics,
not corrections or verified specifications of the original program.

`G3_G5_sensitivity.csv` holds the common 378 pairs fixed. `G5_shared_mask.csv`
distinguishes pair-specific coverage from the common N3 lacuna mask. The parent/subunit
range check is conditional on identical preprocessing, missing-field rules and block
scores. NBSP and ordinary-space differences in Pr1/Pr2 must be removed consistently.
