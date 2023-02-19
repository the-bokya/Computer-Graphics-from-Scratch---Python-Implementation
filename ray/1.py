from canvas import canvas
import numpy as np
class sphereObj:
  def __init__(self, color, R, C):
    self.color = np.array(color)
    self.R = R
    self.C = np.array(C)


O = np.array([0,0,0])
spheres = []
spheres.append(sphereObj([255, 0, 0], 1, [0, -1, 3]))
spheres.append(sphereObj([0, 0, 255], 1, [0, 0, 4]))
spheres.append(sphereObj([0, 255, 0], 1, [-2, 0, 4]))

def trace_ray(O, D, tmin, tmax):
  closest_t = np.inf
  closest_sphere = None
  for sphere in spheres:
    t1, t2 = intersection(O, D, sphere)
    if tmin < t1 < tmax and t1 < closest_t:
      closest_t = t1
      closest_sphere = sphere

    if tmin < t2 < tmax and t2 < closest_t:
      closest_t = t2
      closest_sphere = sphere
  if closest_sphere:
    return closest_sphere.color
  return np.array([255, 255, 255])

def intersection (O, D, sphere):
  C = sphere.C
  R = sphere.R
  CO = O - C
  a = np.dot(D, D)
  b = 2 * np.dot(CO, D)
  c = np.dot(CO, CO) - R**2
  determinant = b**2 - 4 * a * c
  if determinant < 0:
    return np.array([np.inf, np.inf])
  t1 = (-b + np.sqrt(determinant)) / 2*a
  t2 = (-b - np.sqrt(determinant)) / 2*a
  return np.array ([t1, t2])

width = 640
height = 640
screen = canvas (width, height)
def ying():
  for y in range(-height//2, height//2):
    D = screen.canvas_to_viewport(x, y)
    color = trace_ray(O, D, 1, np.inf)
    screen.put_pixel(x, y, color)

for x in range(-width//2, width//2):
  ying()
screen.show()
screen.save("1.jpeg")
