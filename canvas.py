import numpy as np
from PIL import Image as Im
class canvas:
  def __init__(self, width, height):
    self.pixels = np.zeros((height, width, 3), np.uint8)
    self.width = width
    self.height = height
  def put_pixel(self, x, y, color):
    adjusted_x = self.width//2 + x
    adjusted_y = self.height//2 - y
    self.pixels[adjusted_y, adjusted_x] = np.array(color, np.uint8)
  def show(self):
    image = Im.fromarray(self.pixels)
    image.show()

if __name__ == "__main__":
  image = canvas(1920, 1080)
  for i in range(-640, 640):
    for j in range(-360, 360):
      image.put_pixel(i, j, np.uint8(((np.sin(np.array([i, 0.4, 0])/100 + 100 )) / 2) * 255))
  print(image.pixels)
  image.show()
