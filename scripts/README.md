# Audit reproduction with private inputs

Licence: MIT, copyright (c) 2026 Yasutomo Nishi. See LICENSE.

The public release excludes SMSR II text and text-specific legacy restoration
annotations. Use lawfully obtained copies in external private directories:

```sh
python3 scripts/reproduce.py --transcriptions-dir /path/to/private/transcriptions --encoding-dir /path/to/private/annotations
```

Python 3.10+ and a C compiler are required for the full audit. For input-only
verification, add `--check-inputs-only`. With no arguments the runner stops
with an explanation; it does not download or distribute transcription text.
Do not commit private input or generated legacy text. See RIGHTS.md and docs/METHODS.md.
