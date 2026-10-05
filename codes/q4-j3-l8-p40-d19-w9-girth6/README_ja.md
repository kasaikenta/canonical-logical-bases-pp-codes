# [[640,160,19]]

距離とn,k、binary重みは物理qubit単位。GF(4) symbolは2 qubitに展開する。symbol (3,8)-regular、symbol/binary girthはいずれも6、符号率は1/4。完全共役基底の最大binary重みは32。

Hx/HzとLx/Lzをsymbol/binaryの両方で保存した。MatrixMarketの添字は1始まり。GF(4)では1、2=ω、3=ω+1、ω²=ω+1であり、整数演算として扱わない。JSONのbinary_supportは0始まり。

各側のsymbol次数は行8・列3、binary次数は行8/9・列3/4。GF(4)係数1とωのbinary重みは1、ω+1は2。基底重みの分布と各次数の本数はsummary.jsonに記載する。

X/Z双方で重み18以下を排除し、少なくとも一方に重み19の非stabilizer wordを確認した。量子距離はexactである。個別のX/Z区間はsummary.jsonに記載する。

verify.pyはPython標準ライブラリだけで行列、rank、CSS、完全共役性、両girth、上界word、入力・hash・完了根の整合性を再検証する。距離探索を再実行する場合は、同封のC++17 sourceと保存済み入力を使える。完了ログは形式証明支援系の証明書ではない。

construction.jsonにはCPM指数、GF(4)係数、matching、採用基底を保存した。外部の研究用ファイルへの依存を避けた共有用のコピーであり、復号シミュレーションや耐故障性の主張は含まない。

行列と保存証拠の整合性確認：

```sh
python3 verify.py
```

距離排除そのものの再実行：

```sh
c++ -O3 -std=c++17 distance_search.cpp -o distance_search
./distance_search distance/X_input.txt X_recheck.json 18 600
./distance_search distance/Z_input.txt Z_recheck.json 18 600
```

出力のcomplete_exclusion=true、timed_out=false、completed_roots=total_roots=24が必要。timeoutを距離下界として扱わない。再実行結果は元の保存証拠を書き換えない。

分割監査の再実行（physical_search.cppがあれば16根、なければ24根を用いる）：

```sh
python3 recheck_distance.py --seconds 600 --jobs 3
```

完了した根は再利用できる。採用探索器の全根（16または24）・両側の完了が必要であり、未完了の根は時間枠を延ばして再実行する。
