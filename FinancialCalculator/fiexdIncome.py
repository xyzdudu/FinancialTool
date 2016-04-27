# -*- coding: utf-8 -*-
from tkinter import *
import tkinter.messagebox as messagebox

class FiexdIncome(Frame):
	def __init__(self, master=None):
		Frame.__init__(self,master)
		self.pack()
		self.createWidgets()

	def createWidgets(self):
		upframe = Frame(self)
		upframe.pack(side = TOP)

		bottomframe = Frame(self)
		bottomframe.pack(side = BOTTOM)

		self.baseMoneyLabel = Label(upframe, text='起始金额：')
		self.baseMoneyLabel.grid(row=0, column=0)
		self.baseMoney = Entry(upframe, width=20)	#起始金额
		self.baseMoney.grid(row=0, column=1)
		self.annualInterestRateLabel = Label(upframe, text='年利化率：')
		self.annualInterestRateLabel.grid(row=1, column=0)
		self.annualInterestRate = Entry(upframe, width=20)
		self.annualInterestRate.grid(row=1, column=1)
		self.dayLabel = Label(upframe, text='投资期限：')
		self.dayLabel.grid(row=2, column=0)
		self.day = Entry(upframe, width=20)
		self.day.grid(row=2, column=1)
		self.startButton = Button(self, text='计 算', width='8', command=self.onCalculation)
		self.startButton.pack()
		self.expectedReturnLabel = Label(bottomframe, text='预期收益：')
		self.expectedReturnLabel.grid(row=0, column=0)
		self.expectedReturn = Label(bottomframe,text='')
		self.expectedReturn.grid(row=0, column=1)

	def onCalculation(self):
		baseMoney = self.baseMoney.get()
		ann = self.annualInterestRate.get()
		day = self.day.get()

		if baseMoney == '':
			messagebox.showinfo('Warning', '请输入起始金额')
			return
		if ann == '':
			messagebox.showinfo('Warning', '请输入年利化率')
			return
		if day == '':
			messagebox.showinfo('Warning', '请输入投资期限')
			return

		profit = float(baseMoney) * float(ann) / 100 * int(day) / 365

		self.expectedReturn.config(text = '%.2f'%profit)
		

app = FiexdIncome()
# 设置窗口标题:
app.master.title('固定收益计算器')
app.master.geometry('230x120+500+500')
# 主消息循环:
app.mainloop()
