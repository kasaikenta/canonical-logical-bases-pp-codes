# Pair-partition符号から得た正準論理基底の再現データ

本リポジトリは、岡田昂生・笠井健太「Low-Weight Canonical Logical Bases
from Pair-Partition Codes」の再現用資料です。論文に掲載した符号と追加の
完全記述例を合わせた全23符号について、最終二元検査行列 `HX`, `HZ` と
完全正準論理基底 `LX`, `LZ` を収録しています。

`catalog/codes.csv` が収録符号の一覧です。各 `codes/<code-id>/` には、
圧縮済みの四行列 `matrices.npz`、パラメータとハッシュを記録した
`metadata.json`、利用可能な場合は多項式/QC構成入力 `construction.json`
と厳密距離の検証記録があります。四つの二元行列そのものが、符号と
正準基底を一意に定める共通の完全記述です。

全件のCSS条件、核条件、正準条件、ランク、重み、ハッシュは次で確認できます。

```bash
python3 scripts/verify_all.py
```

ファイル仕様は `docs/format.md`、距離証明記録の範囲は
`docs/distance-certification.md` を参照してください。

論文の付録から移した二元多重CPMの明示例は、
[`codes/f2-multicpm-j3-l8-p128-d22-w9/README.md`](codes/f2-multicpm-j3-l8-p128-d22-w9/README.md)
にまとめています。形式的な族、PP親、対分割、調整小行列、正準化、
固定した `[[1024,256,22]]` 例、および厳密距離の検証記録を掲載しています。
付録表に掲載した `P=52` 例と、従属な4ブロック行表示もカタログに収録しています。
