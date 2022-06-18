"""17式ダメージ計算をコンピューターに行わせる。"""
"""tをデッキ1周にかかるターン数とするa1,a2,...,an∈Aを同時に引くと使えない強いカードの集合とする。
P(a)をaのカードを1ターンで引く確率でμ(a)をその時下がる打点とする。Sを強いカードとストライクを
エナジーがあるだけ使用したときの打点とする。"""
"""プレイヤーにデッキのアタックを入力させてt, S, a1,a2,...,an∈A, P(a),μ(a)をマシンに求めさせる。"""
"""#とコメントアウトされている点は主に検証等に使用したコードである。"""
import math
import itertools
from itertools import combinations

"""nは1ターンで用意できるエナジーの数。基本1層で考えるのでn=3であり、2層以降も考えるならn=4,5にすればよい。"""
n=3
"""デッキのアタックから白のストライクを除いたものを全て入力させ、attack_listに格納。lはアタックの枚数。"""
x = 0

attack_list = []

print("デッキのアタックを全て入力してください。ただし白のストライクは除きます")
while x!='':
    x = input()
    attack_list.append(x)

#attack_list = ['bash', 'car', 'ts']

st_count = int(input("白のストライクの枚数を入力してください:"))

#st_count = 5

attack_list.pop()
l = len(attack_list) + st_count

"""アタック以外のカードの枚数を入力させて,(l+SPC)/5でtを求める。SPCはスキルパワー呪いから。"""
SPC = int(input("アタック以外のカードの枚数を入力してください。"))
#SPC = 7
t=(l + SPC)/5
print("3tの値は")
print(t*3)
"""アタックの名前から火力が分かる辞書damage_dict"""
damage_dict ={
    "st":6, 
    "bash":18, 
    "car":20,
    "ts":10,
    "cle":12,#なぎ払いをここでは12と考える
    "feed":10,
    "hemo":11,#ヘモを11と考える
    "ang":6
} 

"""アタックの名前からコストが分かる辞書cost_dict。2つのdictは未完成であり、全てのアタックの情報とはほど遠い。最終的にはtxtファイルにまとめた内容を読み込む形にするのがいい？"""
cost_dict ={
    "st":1,
    "bash":2,
    "car":2,
    "ts":1,
    "cle":1,
    "feed":1,
    "hemo":1,
    "ang":0
}

"""入力させたアタックの名前からそのアタックのコストの合計を求めてCに代入する"""
C = 0
for name in attack_list:
    C +=int(cost_dict[name])
    
"""Cがデッキ1周までに用意できるエナジーより少ない場合その分ストライクを使用するとしてSを考える。"""
if C < n*t:
    b = math.floor(n*t-C)
    if b < st_count:
        use_st = b
    else:
        use_st = st_count

"""Sを算出する"""
S = 0
for name in attack_list:
    S +=int(damage_dict[name])
    
S += 6*use_st
print(S)

"""強いアタックの組み合わせを考える。attack_pairs2, 3, 4, 5はその組み合わせの要素の数"""
d = len(attack_list)
attack_pairs2 = []

for i in range(2,3):
    attack_pairs2 += list(itertools.combinations(attack_list, i))

#print(attack_pairs2),

attack_pairs3 = []

for i in range(3,4):
    attack_pairs3 += list(itertools.combinations(attack_list, i))

#print(attack_pairs3)

attack_pairs4 = []

for i in range(4,5):
    attack_pairs4 += list(itertools.combinations(attack_list, i))

#print(attack_pairs4)

attack_pairs5 = []

for i in range(5,6):
    attack_pairs5 += list(itertools.combinations(attack_list, i))

#print(attack_pairs5)

"""attack_pairsの中に1ターンに使えるエナジー以上を要求する組み合わせがないか確かめる。あったら抜き出しリストmiに代入する。(miは現在使用されていない)redはreductionからきた変数で、
これが起きた際にいくら打点が減るかを表すμ(a)である。Bは最終的な計算結果、PAは17式の計算の最後のS/t(1-P(a1)-P(a2\a1)-...)のP(a1)-P(a2\a1)-...の部分である。"""
mi = []
red = 0
B = 0
PA = 1
for i in attack_pairs2:
    a, b= i
    if cost_dict[a] + cost_dict[b]>=n+1:
        print(a, b)
        print(a, "と", b, "どちらを使いませんか?")
        red = int(damage_dict[input()])
        print(red)
        P = float(input("これが起きる確率を教えてください"))
        PA -=P
        B += P*(S-red)/t
            

for i in attack_pairs3:
    a, b, c= i
    if cost_dict[a] + cost_dict[b] + cost_dict[c]>=n+1:
        print(a, b, c)
        print(a, "と",b,"と", c, "どれを使いませんか?")
        red = int(damage_dict[input()])
        print(red)
        P = float(input("これが起きる確率を教えてください"))
        PA -=P
        B += P*(S-red)/t

"""最終的にストライク4枚や5枚同時引きの確率も計算することで完璧な予測が可能だと考えられる"""
"""
for i in attack_pairs4:
    a, b, c, d= i
    print(a)
    print(b)
    print(c)
    print(d)

for i in attack_pairs5:
    a, b, c, d, e= i
    print(a)
    print(b)
    print(c)
    print(d)
    print(e)

"""
"""結果の出力"""
B += S*PA/t
print(B)
        

