# -*- coding: utf-8 -*-
"""
Created on Sat Jan 30 10:26:25 2021

@author: Robert
"""


import tkinter as tk

def get_selection( name, inputs):#, defaults=[]):
    outputs = []
    def submitFunction():
        sel_idxs = listbox_1.curselection()
        sel_vals = [inputs[i] for i in sel_idxs]
        outputs.extend( sel_vals )
        window_main.destroy()
    
    window_main = tk.Tk(className=name)
    # window_main.geometry('300x250')
    
    title = tk.Label(window_main, text=name)
    title.pack()
    
    listbox_1 = tk.Listbox(window_main, selectmode=tk.MULTIPLE)
    # Populate Listbox
    for i, val in enumerate(inputs):
        listbox_1.insert(i,val)
    # # Set defaults
    # for val in defaults:
    #     i = inputs.index(val)
    #     print(i)
    #     listbox_1.activate(i)
    listbox_1.pack()
    
    submit = tk.Button(window_main, text='Select', command=submitFunction)
    submit.pack()
    
    window_main.mainloop()
    return outputs


if __name__ == '__main__':
    print(get_selection('Selection', list('abcdefg')))#, list('bf')))