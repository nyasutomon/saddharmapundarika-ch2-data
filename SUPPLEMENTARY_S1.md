# Supplementary Material S1 for the DSH manuscript

Zenodo DOI for this version: https://doi.org/10.5281/zenodo.23277312

Release v1.1.0 adds the numerical supplement prepared on 10 October 2026 for
Yasutomo Nishi's manuscript *Textual Variation and Manuscript Transmission in
the Saddharmapuṇḍarīka: A Quantitative Philological Approach*.

Download and extract `Supplementary_Material_S1_v1.1.0.zip`. Its internal README
explains the data, estimators, missing-score rules, resampling, and reproduction.
The supplement contains derived block scores and masks, code for joint block
reweighting and grouping checks, unrounded results, and 600-dpi figure artwork.
It reproduces the statistical layer without access to SMSR transcription text.
The original exported matrices and the earlier audit are retained unchanged.
This is new analysis material, not a replacement for the archived production
outputs and not a complete recovery of the production program.

The ZIP contains no SMSR bulk transcription, text-specific restoration spans,
facsimile images, manuscript text, or private editorial review memorandum.
Text-to-score reconstruction still requires lawful private source inputs.
Numerical metadata includes input filenames and hashes for provenance.

Licences within the supplement: scripts MIT (see scripts/LICENSE); Nishi's
derived data, results, metadata, documentation and figures CC BY 4.0.
No rights to redistribute SMSR texts or facsimiles are granted.

## Reproduce

Install the packages specified in requirements.txt. From the extracted folder:

```sh
python scripts/analyse.py
python scripts/draw_figures.py --font /path/to/font.ttf --bold-font /path/to/bold-font.ttf
```

See README.md inside the ZIP before interpreting intervals or nearest-witness
selection frequencies. The supplied intervals measure conditional stability
under reweighting, not probabilities of genealogy or tests that passage effects
are absent. Original source matrices and the previous audit remain archived at
https://doi.org/10.5281/zenodo.23276190 (v1.0.2).
