import sys,os
import tkinter as tk

class reversi():
    def __init__(self):
        self.row_num = 8

        self.xsize = 600
        self.ysize = 600
        self.tagstr = 'abcdefgh'
        self.item_id = 0
        self.turn = '●'
        self.board = [['##' for i in range (self.row_num + 2)] for j in range(self.row_num + 2)]
        self.board[self.row_num//2][self.row_num//2:self.row_num//2+2] = ['○','●']
        self.board[self.row_num//2+1][self.row_num//2:self.row_num//2+2] = ['●','○']
        self.coordinate = {'x':-1,'y':-1}
        self.dispalay_tk()

    def double_check(self,color):
        if self.board[self.coordinate['y']][self.coordinate['x']] == '##':
            return True
        else:
            print('すでに置いてあります\n\n')
            return False

    def around_check(self,color,x,y):
        empty_cnt = 0
        reversible_cnt = 0
        reversible_tgt = []
        temp_tgt =[]
        pass_flag = False
        for ax in range(x-1,x+2):
            for ay in range(y-1,y+2):
                if ax != x or ay != y:
                    if  self.board[ay][ax] != '##' and self.board[ay][ax] != color:
                        empty_cnt += 1
                        temp_tgt += [[ax,ay]]
        if empty_cnt == 0:
            pass_flag = False
        else:
            reversible_tgt_temp = []
            for bx,by in temp_tgt:
                reversible_tgt_temp = [[bx,by]]
                difx = x - bx
                dify = y - by
                temp_reversible_cnt = 1
                cx = bx - difx
                cy = by - dify
                while True:
                    if cx == 0 or cx == self.row_num + 1 or cy == 0 or cy == self.row_num + 1:
                        break
                    elif self.board[cy][cx] == '##':
                        break
                    elif self.board[cy][cx] != color:
                        temp_reversible_cnt += 1
                        reversible_tgt_temp += [[cx,cy]]
                    else:
                        reversible_cnt += temp_reversible_cnt
                        reversible_tgt += reversible_tgt_temp
                        pass_flag = True
                        break
                    cx = cx - difx
                    cy = cy - dify

        return pass_flag,reversible_cnt,reversible_tgt

    def input_calc(self,color):
        pass_flag = False
        reversible_tgt_sum = []
        for x in range(1,self.row_num + 1):
            for y in range(1,self.row_num + 1):
                if self.board[y][x] == '##':
                    pass_check, reversible_cnt,reversible_tgt = self.around_check(color = color, x = x, y = y)
                    if pass_check:
                        reversible_tgt_sum += reversible_tgt
                        pass_flag = True
        if pass_flag == False:
            self.comment.set('置くところがないためパスします')
            print('置くところがないためパスします')
        while pass_flag:
            if self.double_check(color = color):
                pass_check, reversible_cnt,reversible_tgt = self.around_check(color = color,x = self.coordinate['x'], y = self.coordinate['y'])
                if pass_check:
                    self.board[self.coordinate['y']][self.coordinate['x']] = color
                    for ax,ay in reversible_tgt:
                        self.board[ay][ax] = color
                    print(reversible_tgt)
                    print(str(reversible_cnt) + '個ひっくり返しました')
                    self.comment.set(str(reversible_cnt) + '個ひっくり返しました')
                    pass_flag = False
                    break
                else:
                    print('そこには置けません')
                    self.comment.set('そこには置けません')
                    pass_flag = True
                    break
            else:
                pass_flag = True
                break
        self.refresh_board()
        return pass_flag

    def pressed(self,event):
        self.item_id = self.canvas.find_closest(event.x, event.y)
        self.tag = self.canvas.gettags(self.item_id[0])[0]
        px = self.tag2pos(self.tag[0])
        py = self.tag2pos(self.tag[1])
        print(self.tag,px,py)
        self.coordinate['x'] = px
        self.coordinate['y'] = py
        if self.input_calc(color = self.turn) == False:
            if self.turn == '●':
                self.turn = '○'
            else:
                self.turn = '●'
        self.refresh_board()



    def pos2tag(self, pos):
        for p, t in zip(list(range(1,self.row_num+1)),self.tagstr):
            if pos == p :
                return t

    def tag2pos(self, tag):
        for p, t in zip(list(range(1,self.row_num+1)),self.tagstr):
            if tag == t :
                return p

    def refresh_board(self):
        for num_row in range(1,self.row_num+1):
            for num_line in range(1,self.row_num+1):
                if self.board[num_row][num_line] == '●':
                    tag = self.pos2tag(num_line) + self.pos2tag(num_row)
                    self.canvas.create_oval(*self.tag_pos[tag], fill='black',tags = self.tag)
                elif self.board[num_row][num_line] =='○':
                    tag = self.pos2tag(num_line) + self.pos2tag(num_row)
                    self.canvas.create_oval(*self.tag_pos[tag], fill='white',tags = self.tag)
        self.display_comment()

    def cnt_board(self):
        cnt_b = 0
        cnt_w = 0
        for i in range(1,self.row_num+1):
            cnt_b += self.board[i].count('●')
            cnt_w += self.board[i].count('○')
        return cnt_b, cnt_w

    def display_comment(self):
        cnt_b,cnt_w = self.cnt_board()
        Static1 = tk.Label(text=self.turn+'のターンです')
        Static2 = tk.Label(textvariable=self.comment)
        self.cnt_bw.set('● : ○ = '+str(cnt_b)+' : '+str(cnt_w))
        Static_cntbw = tk.Label(textvariable=self.cnt_bw)
        Static1.place(x=self.xsize/2-200, y=self.ysize -90)
        Static2.place(x=self.xsize/2-200, y=self.ysize -65)
        Static_cntbw.place(x=self.xsize/2, y=self.ysize -90)


    def dispalay_tk(self):
        self.root = tk.Tk()
        self.comment = tk.StringVar()
        self.cnt_bw = tk.StringVar()
        self.comment.set("スタート！！")
        reversi_xsize = 400
        reversi_ysize = 400
        xedge = (self.xsize - reversi_xsize)/2
        yedge = (self.ysize - reversi_ysize)/2
        button = tk.Button(self.root, text = 'Python/Tkinter')
        button.pack()
        self.root.title("リバーシ")
        self.root.minsize(self.xsize, self.ysize)
        self.canvas = tk.Canvas(bg="green", width=reversi_xsize, height=reversi_ysize)
        self.canvas.place(x=xedge,y=yedge)

        self.tag_pos = {}
        for  xstr,x in zip(self.tagstr,list(range(1,self.row_num+1))):
            for ystr,y in zip(self.tagstr,list(range(1,self.row_num+1))):
                self.tag = xstr + ystr
                self.tag_pos[self.tag] = (x-1)*(reversi_ysize/(self.row_num)), (y-1)*(reversi_ysize/(self.row_num)), x*(reversi_ysize/(self.row_num)), y*(reversi_ysize/(self.row_num)),
                self.canvas.create_rectangle(*self.tag_pos[self.tag], fill='green', tags = self.tag)
                self.canvas.tag_bind(self.tag, "<ButtonPress-1>", self.pressed)
        self.refresh_board()


    def run_display(self):
        self.root.mainloop()

reversi = reversi()
reversi.run_display()
