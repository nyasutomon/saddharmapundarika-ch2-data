# サンスクリット法華経第2章 類似度行列と再現性監査

SMSR II 転写の再配布許諾がないため、転写テキスト12ファイルと、本文に対応する
旧文字復元用注釈12ファイルを公開対象から除外しました。この公開リポジトリの
履歴にも収録していません。元の算出結果CSV24ファイルは改変せず公開します。

| 対象 | 公開・ライセンス |
| --- | --- |
| SMSR II 転写 | 非収録。権利は編者・刊行団体その他の権利者に帰属し、再配布は権利者の許諾によります。 |
| `data/matrices/exported/` | 黛氏の了解を得て CC BY 4.0。作成者 Chihiro Mayuzumi、データ整理者 Yasutomo Nishi。 |
| `scripts/` | MIT（Yasutomo Nishi の監査再現コード）。 |
| `docs/`・`metadata/`・`results/`・`data/encoding/` | Yasutomo Nishi の独自の作成部分を CC BY 4.0 で公開。 |

`data/encoding/` には一般的な旧文字対応表だけを収録し、本文ごとの位置注釈は
含めません。監査結果は数値・行数・位置番号・チェックサム等であり、転写本文を
配布するものではありません。ルートの説明・引用・チェックサム資料も CC BY 4.0 です。

再計算には、利用者が適法に保有する転写12ファイルと旧文字復元注釈12ファイルを、
公開リポジトリの外から指定します。公開データだけでは本文に基づく再計算はできません。

```sh
python3 scripts/reproduce.py --transcriptions-dir /path/to/private/transcriptions --encoding-dir /path/to/private/annotations
```

例示パスです。Python 3.10以上とCコンパイラが必要です。
`--check-inputs-only` で入力検証のみ行えます。私有の入力・復元テキストは公開に追加しません。

G3とG5は従来の監査で旧文字単位の各406対が一致しています。他の10行列は監査用の
統一処理で完全一致していません。詳細は docs/METHODS.md と results/reference/ を参照してください。

旧GitHub履歴は `saddharmapundarika-ch2-private-archive` に非公開で保管し、
転写入りの Zenodo v1.0.0（10.5281/zenodo.23275242）はファイル公開を停止しました。
v1.0.1 は転写を含まない公開版です。RIGHTS.md に対象別の条件を記しています。
