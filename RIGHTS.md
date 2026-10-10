# Component-specific rights and licences / 対象別の権利とライセンス

Updated 10 October 2026, effective for the v1.0.1 release and the current branch.
This public repository does not contain SMSR II transcriptions or text-specific restoration annotations. There is no single licence covering the entire repository.

| Component | Attribution / rights | Licence or redistribution condition |
| --- | --- | --- |
| SMSR II transcriptions (excluded from this public release) | SMSR II editors, publishing body and respective rights holders; see `docs/PROVENANCE.md` | No new licence; not distributed. Redistribution requires the rights holders' permission. |
| `data/matrices/exported/` | Chihiro Mayuzumi, creator of the original comparison program and exported results; curated by Yasutomo Nishi | CC BY 4.0, with Mayuzumi's permission confirmed by the depositor on 10 October 2026; see the directory `LICENSE`. |
| `scripts/` | Yasutomo Nishi, original audit reconstruction | MIT; see `scripts/LICENSE`. |
| `docs/`, `metadata/`, `results/`, `data/encoding/` | Yasutomo Nishi, original documentation, manifests, audit results and encoding annotations | CC BY 4.0; see the `LICENSE` in each directory. |
| Root documentation and citation/checksum metadata | Yasutomo Nishi, original contributions | CC BY 4.0 under the same terms as `docs/LICENSE`. |

## SMSR II transcriptions / 転写データ

The rights in the SMSR II transcription remain with its editors, publishing
body and respective rights holders. This repository grants no new reuse
licence for `data/transcriptions/`. Redistribution requires the rights
holders' permission; existing permissions and statutory exceptions are unchanged.
Public access does not itself constitute a redistribution licence.

**SMSR II の転写データの権利は、編者・刊行団体その他の権利者に帰属します。
転写データに新しいライセンスは付けません。再配布は権利者の許諾によります。
既存の許諾および法令上認められる利用は変更しません。**

## Original exported matrices / 元の算出結果

Chihiro Mayuzumi is credited as the creator of the original comparison program
and exported results. The depositor confirmed his permission on 10 October 2026
to distribute the 24 original CSV exports under CC BY 4.0. Credit Mayuzumi and
Nishi's dataset curation, cite the version/DOI, link the licence and identify
changes. The permission does not extend to the underlying SMSR II transcription
or the original program source, which is not included.

**元の算出結果24ファイルは、黛氏の了解を得て CC BY 4.0 で公開します。
作成者として Chihiro Mayuzumi（黛氏）を明記し、データ整理者として
Yasutomo Nishi を記します。元のプログラム本体は含まれていません。**

## Audit scripts / 監査スクリプト

The independently prepared audit reconstruction in `scripts/` is available
under the MIT licence, copyright (c) 2026 Yasutomo Nishi. It is distinct from
Mayuzumi's original production program. The full MIT terms are in `scripts/LICENSE`.

## Documentation, metadata, audit results and encoding annotations

Nishi's original contributions in `docs/`, `metadata/`, `results/` and
`data/encoding/` are licensed under CC BY 4.0. Root documentation and citation/
checksum metadata are covered on the same basis. Cite Nishi, the dataset
version and DOI, retain the licence link and attribution, and indicate changes.
Quoted or incorporated third-party material retains its existing rights.
The encoding annotations do not grant a licence for the source text they restore.

CC BY 4.0: https://creativecommons.org/licenses/by/4.0/
Full legal terms: https://creativecommons.org/licenses/by/4.0/legalcode.en
MIT terms: `scripts/LICENSE`; official text: https://opensource.org/license/mit

## Excluded source material and previous archives

The 12 SMSR II UTF8 transcriptions and the 12 text-specific legacy restoration
annotation files are excluded from this public release. They are also absent
from this repository's Git history, which starts with the clean release.
`data/transcriptions/` contains only a notice, not transcription text.

The former repository and its transcription-bearing history are privately
retained as `nyasutomon/saddharmapundarika-ch2-private-archive`. Files of the
previous Zenodo v1.0.0 record (10.5281/zenodo.23275242) were restricted on
10 October 2026 because redistribution permission has not been obtained.
This public replacement does not distribute those files.

Numerical matrix exports have Chihiro Mayuzumi's permission for CC BY 4.0.
The public code uses external, lawfully obtained private transcriptions and
restoration annotations. Do not commit those inputs or generated text to this
public repository. Checksums and numerical results do not grant source-text rights.


## Numerical supplement v1.1.0

The component licences inside Supplementary_Material_S1_v1.1.0.zip apply: scripts are MIT; Nishi's original derived numeric data, results, metadata, documentation and figures are CC BY 4.0. The ZIP excludes SMSR transcription texts, text-specific restoration annotations and facsimile images. The supplement grants no rights over excluded inputs.
