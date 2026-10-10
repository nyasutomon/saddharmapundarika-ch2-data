# Saddharmapuṇḍarīka Chapter 2 data and reproducibility audit

## New numerical supplement v1.1.0

Zenodo v1.1.0 DOI: https://doi.org/10.5281/zenodo.23277312

[Supplementary Material S1](SUPPLEMENTARY_S1.md) contains derived block scores, masks, joint block reweighting and grouping code, unrounded results, and 600-dpi figures. [Download the supplement](Supplementary_Material_S1_v1.1.0.zip). No SMSR transcription or facsimile images are included. The DOI below identifies the earlier v1.0.2 audit, not the new supplement.


[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23276190.svg)](https://doi.org/10.5281/zenodo.23276190)

Automatically archived v1.0.2: https://doi.org/10.5281/zenodo.23276190

Previously archived v1.0.1 (transcriptions excluded): https://doi.org/10.5281/zenodo.23275839

Original exported similarity matrices and an
independent numerical audit supporting Yasutomo Nishi's ASCJ 2027 research.
The corpus contains 33 manuscript witnesses and an additional KN reference row.
The principal chapter-wide interpretation excludes F and M, leaving 31 witnesses.

Public repository: https://github.com/nyasutomon/saddharmapundarika-ch2-matrices

v1.0.2 updates automatic archival integration and citation metadata. Numerical data and source exclusions are unchanged.

## Contents

- SMSR II transcription texts: excluded; `data/transcriptions/` contains only a notice.
- `data/matrices/exported/`: all 24 supplied CSV outputs, unchanged.
- `data/encoding/`: generic character mapping only; text-specific restoration annotations are excluded.
- `results/reference/`: published audit results, distinct from the original exports.
- `scripts/`: portable audit reconstruction using Python's standard library and C.
- `metadata/`: source checksums and encoding provenance, without private local paths.
- `docs/`: provenance, data structure, numerical limitations and reproduction rules.

## Reproduce the audit with private inputs

Requirements: Python 3.10 or later, a C compiler, and lawfully obtained private
copies of the 12 UTF8 transcriptions plus the 12 legacy restoration annotation files.
The transcriptions and text-specific annotations are not downloadable here.

```sh
python3 scripts/reproduce.py --transcriptions-dir /path/to/private/transcriptions --encoding-dir /path/to/private/annotations
```

Paths are examples, not depositor paths. The runner validates the 24 public CSV
exports and the 12 external UTF8 inputs against the input manifest, restores
legacy font units privately, runs the audit and checks the numerical reference
results. Use `--check-inputs-only` to validate inputs without running the analysis.
Generated inputs/results are ignored; no network or account credentials are used.
This public release alone cannot reproduce text-based scores without private inputs.

## What is and is not reproduced

G3 and G5 each reproduce all 406 available exported pair scores in the original
font-character representation. On the same 378 pairs their equal-block means
are 90.296414% and 80.752580%. This set includes D2 and O.

The other ten export units are not fully reproduced by the uniform audit baseline.
This release records those differences rather than replacing the original values.
UTF8 conversion is verified, but measuring Unicode code points instead of legacy
font units changes the numerical values. The distinction must be retained.

The original percentage-formatted ranking files have 22 adjacent numeric order
inversions: Whole 2, Prose 2 and Pr3 18. Numerically recomputed rankings are separate
audit outputs; the original ranking files remain unchanged.

The files named `correlation_matrix` contain edit similarities from 0 to 1,
not Pearson correlations. Zero cells associated with unavailable text are not
counted as reproduced measurements. See `docs/DATA_DICTIONARY.md` and
`docs/METHODS.md` before interpreting a matrix.

## Citation and component licences

See `CITATION.cff` for the curator and version, `docs/PROVENANCE.md` for source
attribution, and `RIGHTS.md` for the complete component-specific policy.

| Directory | Licence / condition |
| --- | --- |
| SMSR II transcriptions | Excluded; no redistribution licence granted. |
| `data/matrices/exported/` | CC BY 4.0 with Chihiro Mayuzumi's permission; credit Mayuzumi as creator and Nishi as curator. |
| `scripts/` | MIT, copyright (c) 2026 Yasutomo Nishi. |
| `docs/`, `metadata/`, `results/`, `data/encoding/` | CC BY 4.0, Nishi's original contributions. |

Root documentation and citation/checksum metadata are also CC BY 4.0.
Third-party source material retains its existing rights. The paper, presentation
and manuscript facsimiles are not included.

v1.0.1 excludes the 12 transcription texts and the 12 text-specific restoration
annotation files and has a clean Git history. The earlier repository is privately
retained, and files of Zenodo v1.0.0 (10.5281/zenodo.23275242) are restricted.
The public matrices and original audit materials use the component licences above.
See RIGHTS.md; a single repository-wide licence does not apply.
