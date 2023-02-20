"""
This file has the lighting for diffusion implementation
"""
from canvas import canvas
import numpy as np

class light_object:
  def __init__(self, **kwargs):
    self.type = kwargs["type"]
    self.intensity = kwargs["intensity"]
    if self.type == "point":
      self.position = np.array(kwargs["position"])
    if self.type == "directional":
      self.direction = np.array(kwargs["direction"])
  
  def calc_intensity(self, P, N, V, s):
    out = 0
    if self.type == "ambient":
      out = self.intensity
      return out
    if self.type == "point":
      L = self.position - P
    if self.type == "directional":
      L = self.direction
    #diffuse
    out = np.dot(N, L) 
    out = max(0, out)
    out /= (np.linalg.norm(L))
    out *= self.intensity
    #specular
    R = 2 * np.dot(N, L) * N - L
    spec = (np.dot(R, V) / (np.linalg.norm(R) * np.linalg.norm(V))) ** s
    spec = max(0, spec)
    out += spec * self.intensity
    return out

lights = []
lights.append(light_object(type="ambient", intensity=0.2))
lights.append(light_object(type="point", intensity=0.6, position=[2, 1, 0]))
lights.append(light_object(type="directional", intensity=0.2, direction=[1, 4, 4]))

class sphere_object:
  def __init__(self, color, R, C, specular):
    self.color = np.array(color)
    self.R = R
    self.C = np.array(C)
    self.specular = specular


O = np.array([0,0,0])
spheres = []
spheres.append(sphere_object([255, 0, 0], 1, [0, -1, 3], 500))
spheres.append(sphere_object([0, 0, 255], 1, [2, 0, 4], 500))
spheres.append(sphere_object([0, 255, 0], 1, [-2, 0, 4], 10))
spheres.append(sphere_object([255, 255, 0], 5000, [0, -5001, 0], 1000))

def compute_lighting(P, N, V, s):
  intensity = 0
  for light in lights:
    intensity += light.calc_intensity(P, N, V, s)
  intensity = min(1, intensity)
  return intensity
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
    P = O + closest_t * D
    N = P - closest_sphere.C
    N = N/np.linalg.norm(N)
    s = closest_sphere.specular
    return closest_sphere.color * compute_lighting(P, N, -D, s)
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

width = 1024
height = 1024
screen = canvas (width, height)

for x in range(-width//2, width//2):
  print(x)
  for y in range(-height//2, height//2):
    D = screen.canvas_to_viewport(x, y)
    color = trace_ray(O, D, 1, np.inf)
    screen.put_pixel(x, y, color)
screen.show()
screen.save("2.jpeg")
