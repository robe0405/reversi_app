# 二人プレイ
import numpy as np

"""
定数宣言
"""
EMPTY = 0 # 空きマス
WHITE = -1 # 白石
BLACK = 1 # 黒石
WALL = 2 # 壁
BOARD_SIZE = 8 # ボードのサイズ

# 方向(2進数)
NONE = 0
LEFT = 2**0 # =1
UPPER_LEFT = 2**1 # =2
UPPER = 2**2 # =4
UPPER_RIGHT = 2**3 # =8
RIGHT = 2**4 # =16
LOWER_RIGHT = 2**5 # =32
LOWER = 2**6 # =64
LOWER_LEFT = 2**7 # =128

Max_TURNS = 60

"""
ボードの表現
"""
class Board:

    def __init__(self):
        # 全マスを空きマスに設定
        self.RawBoard = np.zeros((BOARD_SIZE + 2, BOARD_SIZE + 2), dtype=int)
        self.MovableDir = np.zeros((BOARD_SIZE + 2, BOARD_SIZE + 2), dtype=int)
        # 壁の設定
        self.RawBoard[0, :] = WALL
        self.RawBoard[:, 0] = WALL
        self.RawBoard[BOARD_SIZE + 1, :] = WALL
        self.RawBoard[:, BOARD_SIZE + 1] = WALL
        # 初期配置
        self.RawBoard[4, 4] = WHITE
        self.RawBoard[5, 5] = WHITE
        self.RawBoard[4, 5] = BLACK
        self.RawBoard[5, 4] = BLACK
        # 手番
        self.Turns = 0
        # 色
        self.CurrentColor = BLACK

    """
    どの方向に石が裏返るかをチェック
    """
    def checkMobility(self, x, y, color):
        # 注目しているマスの裏返せる方向の情報が入る
        dir = 0
        # 既に石がある場合はダメ
        if(self.RawBoard[x, y] != EMPTY):
            return dir

        ## 上
        if(self.RawBoard[x - 1, y] == - color):
            x_tmp = x - 2
            y_tmp = y
            while self.RawBoard[x_tmp, y_tmp] == - color:
                x_tmp -= 1
            if self.RawBoard[x_tmp, y_tmp] == color:
                dir = dir | UPPER

        ## 左上
        if(self.RawBoard[x - 1, y - 1] == - color):
            x_tmp = x - 2
            y_tmp = y - 2
            while self.RawBoard[x_tmp, y_tmp] == - color:
                x_tmp -= 1
                y_tmp -= 1
            if self.RawBoard[x_tmp, y_tmp] == color:
                dir = dir | UPPER_LEFT

        ## 左
        if(self.RawBoard[x, y - 1] == - color):
            x_tmp = x
            y_tmp = y - 2
            while self.RawBoard[x_tmp, y_tmp] == - color:
                y_tmp -= 1
            if self.RawBoard[x_tmp, y_tmp] == color:
                dir = dir | LEFT

        ## 左下
        if(self.RawBoard[x + 1, y - 1] == - color):
            x_tmp = x + 2
            y_tmp = y - 2
            while self.RawBoard[x_tmp, y_tmp] == - color:
                x_tmp += 1
                y_tmp -= 1
            if self.RawBoard[x_tmp, y_tmp] == color:
                dir = dir | LOWER_LEFT

        ## 下
        if(self.RawBoard[x + 1, y] == - color):
            x_tmp = x + 2
            y_tmp = y
            while self.RawBoard[x_tmp, y_tmp] == - color:
                x_tmp += 1
            if self.RawBoard[x_tmp, y_tmp] == color:
                dir = dir | LOWER

        ## 右下
        if(self.RawBoard[x + 1, y + 1] == - color):
            x_tmp = x + 2
            y_tmp = y + 2
            while self.RawBoard[x_tmp, y_tmp] == - color:
                x_tmp += 1
                y_tmp += 1
            if self.RawBoard[x_tmp, y_tmp] == color:
                dir = dir | LOWER_RIGHT

        ## 右
        if(self.RawBoard[x, y + 1] == - color):
            x_tmp = x
            y_tmp = y + 2
            while self.RawBoard[x_tmp, y_tmp] == - color:
                y_tmp += 1
            if self.RawBoard[x_tmp, y_tmp] == color:
                dir = dir | RIGHT

        ## 右上
        if(self.RawBoard[x - 1, y + 1] == - color):
            x_tmp = x - 2
            y_tmp = y + 2
            while self.RawBoard[x_tmp, y_tmp] == - color:
                x_tmp -= 1
                y_tmp += 1
            if self.RawBoard[x_tmp, y_tmp] == color:
                dir = dir | UPPER_RIGHT

        return dir

    """
    石を置くことによる盤面の変化をボードに反映
    """
    def flipDiscs(self, x, y):
        # 選んだ場所のdirを取得
        self.hintMovable()
        dir = self.MovableDir[x, y]
        # 石を置く
        self.RawBoard[x, y] = self.CurrentColor
        ## 上
        if dir & UPPER: # AND演算子
            x_tmp = x - 1
            # 相手の石がある限りループが回る
            while self.RawBoard[x_tmp, y] == - self.CurrentColor:
                # 相手の石があるマスを自分の石の色に塗り替えている
                self.RawBoard[x_tmp, y] = self.CurrentColor
                # さらに1マス左に進めてループを回す
                x_tmp -= 1

        ## 左上
        if dir & UPPER_LEFT:
            x_tmp = x - 1
            y_tmp = y - 1
            while self.RawBoard[x_tmp, y_tmp] == - self.CurrentColor:
                self.RawBoard[x_tmp, y_tmp] = self.CurrentColor
                x_tmp -= 1
                y_tmp -= 1

        ## 左
        if dir & LEFT:
            y_tmp = y - 1
            while self.RawBoard[x, y_tmp] == - self.CurrentColor:
                self.RawBoard[x, y_tmp] = self.CurrentColor
                y_tmp -= 1

        ## 左下
        if dir & LOWER_LEFT:
            x_tmp = x + 1
            y_tmp = y - 1
            while self.RawBoard[x_tmp, y_tmp] == - self.CurrentColor:
                self.RawBoard[x_tmp, y_tmp] = self.CurrentColor
                x_tmp += 1
                y_tmp -= 1

        ## 下
        if dir & LOWER:
            x_tmp = x + 1
            while self.RawBoard[x_tmp, y] == - self.CurrentColor:
                self.RawBoard[x_tmp, y] = self.CurrentColor
                x_tmp += 1

        ## 右下
        if dir & LOWER_RIGHT:
            x_tmp = x + 1
            y_tmp = y + 1
            while self.RawBoard[x_tmp, y_tmp] == - self.CurrentColor:
                self.RawBoard[x_tmp, y_tmp] = self.CurrentColor
                x_tmp += 1
                y_tmp += 1

        ## 右
        if dir & RIGHT:
            y_tmp = y + 1
            while self.RawBoard[x, y_tmp] == - self.CurrentColor:
                self.RawBoard[x, y_tmp] = self.CurrentColor
                y_tmp += 1

        ## 右上
        if dir & UPPER_RIGHT:
            x_tmp = x - 1
            y_tmp = y + 1
            while self.RawBoard[x_tmp, y_tmp] == - self.CurrentColor:
                self.RawBoard[x_tmp, y_tmp] = self.CurrentColor
                x_tmp -= 1
                y_tmp += 1

    """
    石を置く
    """
    def move(self, x, y):
        # 石を裏返す
        self.initMovable(x, y)
        if self.initMovable(x, y):
            self.flipDiscs(x, y)
            self.Turns += 1
            self.CurrentColor = -self.CurrentColor
            return True
        else:
            print("----------------")
            print("石を置けません")
            print("----------------")
            return False

    def initMovable(self, x, y):
        # checkMobility関数の実行
        dir = self.checkMobility(x, y, self.CurrentColor)
        if dir > 0:
            return True
        else:
            return False

    """
    どの位置に石を置けるかチェック
    """
    def hintMovable(self):
        for i in range(1, BOARD_SIZE + 1):
            for l in range(1, BOARD_SIZE + 1):
                # checkMobility関数の実行
                dir = self.checkMobility(i, l, self.CurrentColor)
                # 各マスのMovableDirにそれぞれのdirを代入
                self.MovableDir[i, l] = dir

    """
    オセロ盤面の表示
    """
    def display(self):
        # 横軸
        print('  a  b  c  d  e  f  g  h ')
        # 縦軸
        for y in range(1, 9):
            print(y, end="")
            # マスの種類(数値)をgridに代入
            for x in range(1, 9):
                grid = self.RawBoard[x, y]
                # マスの種類によって表示を変化
                if grid == EMPTY: # 空きマス
                    print(' □ ', end="")
                elif grid == WHITE: # 白石
                    print(' ● ', end="")
                elif grid == BLACK: # 黒石
                    print(' x ', end="")
            # 最後に改行
            print()
    def hint_display(self):
        # 横軸
        print('  a  b  c  d  e  f  g  h ')
        # 縦軸
        for y in range(1, 9):
            print(y, end="")
            # マスの種類(数値)をgridに代入
            for x in range(1, 9):
                grid = self.MovableDir[x, y]
                # マスの種類によって表示を変化
                if grid == EMPTY: # 空きマス
                    print(' □ ', end="")
                else:
                    print(' ★ ', end="")
            # 最後に改行
            print()

    """
    入力・チェック
    """
    def main_input(self):
        # 手を入力
        global input_al, input_num
        input_al = "abcdefgh"
        input_num = "12345678"
        input_ans = input("石を置く場所を選択してください: ")
        if self.check_input(input_ans):
            # displayの影響でx,yが逆になるからここでも逆にする
            input_x = input_al.index(input_ans[0]) + 1
            input_y = input_num.index(input_ans[1]) + 1
            self.move(input_x, input_y)
        else:
            print("-----------------------------------")
            print("正しい形式(例:f5)で入力してください")
            print("-----------------------------------")
            return False

    def check_input(self, input_ans):
        if not input_ans:
            return False
        if input_ans[0] in input_al:
            if input_ans[1] in input_num:
                return True
        return False

    """
    終局判定
    """
    def GameOver(self):
        # 60手に達していたらゲーム終了
        if self.Turns >= Max_TURNS:
            return True
        # (現在の手番)打てる手がある場合はゲームを終了しない
        if self.MovableDir[:, :].any():
            return False
        # (相手の手番)打てる手がある場合はゲームを終了しない
        for i in range(1, BOARD_SIZE + 1):
            for l in range(1, BOARD_SIZE + 1):
                if self.checkMobility(i, l, -self.CurrentColor) != 0:
                    return False
        # ここまでたどり着いたらゲームは終わり
        return True

def main():
    while True:
        board.display()
        if board.CurrentColor == BLACK:
            print('黒の番です(x)')
        else:
            print('白の番です(●)')
        hint = input("ヒント(yes): ")
        if hint == "end":
            break
        # ヒントの表示
        board.hintMovable()
        if hint in ["yes", "y"]:
            board.hint_display()
        # パス
        if not board.MovableDir[:, :].any():
            if board.CurrentColor == BLACK:
                print('黒はパスしました')
            else:
                print('白はパスしました')
            board.CurrentColor = -board.CurrentColor
            continue
        # 入力
        if board.main_input() == False:
            continue
        # 終局判定
        if board.GameOver():
            board.display()
            print('おわり')
            break



board = Board()
main()
"""
勝敗
"""
print("------------------------------------------")
# 各色の数
count_black = np.count_nonzero(board.RawBoard[:, :] == BLACK)
count_white = np.count_nonzero(board.RawBoard[:, :] == WHITE)
print('黒: ', count_black)
print('白: ', count_white)
# 勝敗
dif = count_black - count_white
if dif > 0:
    print('黒の勝ち!')
elif dif < 0:
    print('白の勝ち!')
else:
    print('引き分け!')
