import tkinter as tk


class PromotionButton(tk.Button):
    def __init__(self, *args, **kwargs):
        tk.Button.__init__(self, *args, **kwargs)
        self['width'] = max(10, self.master['width'])
        self['height'] = max(2, self.master['height'])
        self.fontsize = '19'
        self['font'] = 'Arial ' + self.fontsize
        self['justify'] = tk.CENTER
        # self.tk = tk
        # self.promote_button = tk.Button(frame, text=text, command=command)
        # ,
        #           width=self.width, height=self.height,
        #           font=self.font, justify=self.justify)
