import tkinter as tk
from PIL import ImageGrab
import time

class ScreenCaptureApp:
    def __init__(self,root):
        self.root = root
        self.root.attributes('-fullscreen',True) #Makes the window fullscreen
        self.root.attributes('-alpha', 0.3) #Should set it to transparent
        self.root.attributes('-topmost',True) #always hoist as top window app
        self.root.bind('<ButtonPress-1>', self.on_mouse_down)
        self.root.bind('<B1-Motion>', self.on_mouse_drag)
        self.root.bind('<ButtonRelease-1>', self.on_mouse_up)
        self.canvas = tk.Canvas(root,cursor='cross',bg='white')
        self.canvas.pack(fill='both',expand=True)
        self.rect= None
        self.start_x = None
        self.start_y = None
        self.screenshot = None
    
    def on_mouse_down(self, event):
        self.start_x = event.x
        self.start_y = event.y
        if not self.rect:
            self.rect = self.canvas.create_rectangle(self.start_x,self.start_y,self.start_x,self.start_y,outline='blue',width=2)
    
    def on_mouse_drag(self,event):
        self.canvas.coords(self.rect,self.start_x,self.start_y,event.x,event.y)
    
    def on_mouse_up(self,event):
        end_x = event.x
        end_y = event.y

        self.capture_screen(self.start_x,self.start_y,end_x,end_y)
        self.root.destroy()

    def capture_screen(self,start_x,start_y,end_x,end_y):
        self.root.withdraw()
        time.sleep(0.1)
        
        x1 = min(start_x,end_x)
        y1 = min(start_y,end_y)
        x2 = max(start_x,end_x)
        y2 = max(start_y,end_y)
        bbox = (x1,y1,x2,y2)
        time.sleep(0.1)
        screenshot = ImageGrab.grab(bbox)
        self.screenshot = screenshot
        screenshot.save('screen-shot.png')
    
if __name__ == '__main__':
    root = tk.Tk()
    app = ScreenCaptureApp(root)
    root.mainloop()