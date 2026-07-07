# 作業手順
## 起動
仮想環境のアクティベート
```command
source ~/Arm_Lib/dofbot-env/bin/activate
```
jyupter Nootbookの起動
```command
jupyter lab --ip=0.0.0.0 --no-browser
```
※多分途中でトークン（パスワード）の要求がされるがターミナルに表示される<トークン>を入力
```
<URL>?token=<トークン>
```
## 終了
jyupter Nootbookの終了
```
Ctrl + C
```
仮想環境のディアクティベート
```
deactivate
```
