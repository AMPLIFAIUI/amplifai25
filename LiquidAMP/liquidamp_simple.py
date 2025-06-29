# liquidamp_simple.py - WORKING VERSION
import tkinter as tk
import numpy as np

class LiquidAMP:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Liquid AMP")
        self.canvas = tk.Canvas(self.root, width=800, height=600, bg='black')
        self.canvas.pack()
        self.particles = [{
            'x': np.random.randint(0, 800),
            'y': np.random.randint(0, 600),
            'vx': np.random.uniform(-1, 1),
            'vy': np.random.uniform(-1, 1)
        } for _ in range(100)]
        self.animate()
        self.root.mainloop()

    def animate(self):
        self.canvas.delete("all")
        for p in self.particles:
            p['x'] += p['vx']
            p['y'] += p['vy']
            # Bounce off walls
            if p['x'] <= 0 or p['x'] >= 800: p['vx'] *= -1
            if p['y'] <= 0 or p['y'] >= 600: p['vy'] *= -1
            self.canvas.create_oval(
                p['x']-3, p['y']-3,
                p['x']+3, p['y']+3,
                fill='cyan', outline=''
            )
        self.root.after(30, self.animate)

if __name__ == "__main__":
    LiquidAMP()