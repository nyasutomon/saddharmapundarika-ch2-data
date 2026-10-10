# Reproduction method and limitations

For cleaned corresponding field strings a and b, the audit uses
`100 * (1 - Levenshtein(a, b) / max(len(a), len(b)))`.
Quotation marks, parenthesized notes, numerical references, whitespace including
NBSP, digits and delimiters are removed. Surviving letters in nonnumeric restoration
brackets are retained. Spelling, sandhi and vocabulary are not normalized.
The exact cleaning patterns and unit-counting choices are in `scripts/audit.py`.

Fields with `<LAC>` on either side are excluded. Two cleaned empty fields are
excluded; one-sided cleaned emptiness scores zero. Retained field scores are
averaged within each block and retained block scores are averaged equally.
In the strict audit baseline, unequal TAB-field counts cause exclusion of the pair's
whole block. This exclusion is an audit policy, not an established production rule.

Both original font-symbol and Unicode-code-point units are computed. Encoding-span
annotations are required for the original units because one font symbol can expand
into `ch`, `dh`, `ai`, `au`, `ṃy`, etc. A simple UTF8 character count would change
the measure even if the conversion was completely correct.

G3/G5 sensitivity uses the common 28 witnesses and 378 pairs, including D2 and O.
Each method first computes a block score and then averages blocks: equal field weights,
field weights from the longer string's length, or within-block concatenation.
For the G5 matched-coverage comparisons, a common lacuna mask retains 8 blocks / 15 fields.
The A2-versus-T8 margin around P3 is particularly small in the Unicode calculation.

All 406 positive G3 scores and all 406 G5 scores match their exports under legacy
strict scoring. No uniform tested policy reproduces all other units. Flagged
alignment, blank-field, sparse-coverage and aggregation cases are reported in the
reference results. Those results must not be substituted as corrected official matrices.

If a parent matrix is obtained from the same retained block scores as its subunits,
its score must lie within the subunit range. In the set excluding F and M, one verse
pair and 37 prose pairs lie outside that range. Different production rules or source
versions could account for this; the original program and settings are needed.

The C distance scorer is checked against a separate dynamic-programming reference
on known examples and seeded cases before the full audit. The runner verifies
the recalculated CSV and JSON outputs against this release's reference records.
That verification repeats the audit, not the original production workflow.

## Private-input boundary in v1.0.1

The public repository excludes all SMSR II transcription files and text-specific
restoration annotations. The runner takes them from external private directories
using --transcriptions-dir and --encoding-dir. Hashes are validated against
the published input manifest. Only numerical reference results and generic
character mapping are public. Without the external inputs, text-based results
cannot be recomputed from this public release alone.
