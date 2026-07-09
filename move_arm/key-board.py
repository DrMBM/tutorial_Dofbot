import ipywidgets as widgets
from IPython.display import display

# 入力ボックスを作成
text_input = widgets.Text(
    value='',
    placeholder='ここにカーソルを合わせてキーを押してください',
    description='操作窓:',
)

# 文字が入力された瞬間に動く処理
def handle_keypress(change):
    val = change['new'].lower()
    if not val:
        return
    
    # 打ち込まれた最後の1文字を判定
    key = val[-1]
    
    if key == 'w':
         print("wキーが押されました")
    elif key == 'a':
         print("aキーが押されました")
    elif key == 's':
         print("sキーが押されました")
    elif key == 'd':
         print("dキーが押されました")
    elif key == 'q':
         print("qキーが押されました（終了）")
         text_input.close() # 入力ボックスを閉じる
         return
        
    # 入力された文字を自動で消去して、次の入力を待ち受ける
    text_input.value = ''

# ボックスの文字変化を監視する設定
text_input.observe(handle_keypress, names='value')

# 画面に表示
display(text_input)