import numpy as np
import tkinter as tk
from tkinter import colorchooser, Scale
from PIL import Image, ImageTk

class VitraySimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Vitray Işık Simülasyonu")
        
        # Varsayılan ayarlar
        self.grid_size = 10
        self.cell_size = 40
        self.colors = [(255, 0, 0), (0, 0, 255), (0, 255, 0), (255, 255, 0)]
        self.current_color = (255, 0, 0)  # Kırmızı
        self.light_intensity = 0.7
        
        # Canvas oluştur
        self.canvas = tk.Canvas(root, width=self.grid_size*self.cell_size, 
                               height=self.grid_size*self.cell_size, bg="white")
        self.canvas.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Kontrol paneli
        self.controls = tk.Frame(root)
        self.controls.pack(side=tk.RIGHT, padx=10)
        
        # Renk seçici
        tk.Button(self.controls, text="Renk Seç", command=self.choose_color).pack(pady=5)
        
        # Işık şiddeti kaydırıcı
        tk.Label(self.controls, text="Işık Şiddeti:").pack()
        self.light_slider = Scale(self.controls, from_=0.1, to=1.0, resolution=0.1, 
                                orient=tk.HORIZONTAL, command=self.update_light)
        self.light_slider.set(self.light_intensity)
        self.light_slider.pack()
        
        # Temizle butonu
        tk.Button(self.controls, text="Temizle", command=self.clear_canvas).pack(pady=5)
        
        # Çizim için bağlantılar
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<Button-1>", self.paint)
        
        # Başlangıç grid'i
        self.grid = np.zeros((self.grid_size, self.grid_size, 3), dtype=np.uint8)
        self.update_canvas()
    
    def choose_color(self):
        color = colorchooser.askcolor()[0]
        if color:
            self.current_color = tuple(map(int, color))
    
    def paint(self, event):
        x, y = event.x // self.cell_size, event.y // self.cell_size
        if 0 <= x < self.grid_size and 0 <= y < self.grid_size:
            self.grid[y, x] = self.current_color
            self.update_canvas()
    
    def update_light(self, val):
        self.light_intensity = float(val)
        self.update_canvas()
    
    def clear_canvas(self):
        self.grid.fill(0)
        self.update_canvas()
    
    def update_canvas(self):
        # Işık efektini uygula
        lit_grid = np.clip(self.grid * self.light_intensity, 0, 255).astype(np.uint8)
        
        # Görseli oluştur
        img = Image.fromarray(lit_grid, 'RGB')
        img = img.resize((self.grid_size*self.cell_size, self.grid_size*self.cell_size), Image.NEAREST)
        self.tk_img = ImageTk.PhotoImage(img)
        
        # Canvas'ı güncelle
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_img)
        
        # Grid çizgileri
        for i in range(self.grid_size + 1):
            self.canvas.create_line(i * self.cell_size, 0, i * self.cell_size, 
                                  self.grid_size * self.cell_size, fill="gray")
            self.canvas.create_line(0, i * self.cell_size, self.grid_size * self.cell_size, 
                                  i * self.cell_size, fill="gray")

# Uygulamayı başlat
root = tk.Tk()
app = VitraySimulator(root)
root.mainloop()