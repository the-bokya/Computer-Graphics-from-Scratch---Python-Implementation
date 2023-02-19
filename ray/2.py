"""
This file has the lighting implementation
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
  
  def calc_intensity(self, P, N):
    out = 0
    if self.type == "ambient":
      out = self.intensity
      return out
    if self.type == "point":
      L = self.position - P
    if self.type == "directional":
      L = self.direction
    out = np.dot(N, L) 
    out = max(0, out)
    out /= (np.linalg.norm(N) * np.linalg.norm(L))
    out *= self.intensity
    return out

lights = []
lights.append(light_object(type="ambient", intensity=0.2))
lights.append(light_object(type="point", intensity=0.6, position=[2, 1, 0]))
lights.append(light_object(type="directional", intensity=0.2, direction=[1, 4, 4]))

class sphere_object:
  def __init__(self, color, R, C):
    self.color = np.array(color)
    self.R = R
    self.C = np.array(C)


O = np.array([0,0,0])
spheres = []
spheres.append(sphere_object([255, 0, 0], 1, [0, -1, 3]))
spheres.append(sphere_object([0, 0, 255], 1, [2, 0, 4]))
spheres.append(sphere_object([0, 255, 0], 1, [-2, 0, 4]))
spheres.append(sphere_object([255, 255, 0], 5000, [0, -5001, 0]))

def compute_lighting(P, N):
  intensity = 0
  for light in lights:
    intensity += light.calc_intensity(P, N)
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
    P = closest_t * D
    N = P - closest_sphere.C
    N = N/np.linalg.norm(N)
    return closest_sphere.color * compute_lighting(P, N)
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

width = 256
height = 256
screen = canvas (width, height)

for x in range(-width//2, width//2):
  for y in range(-height//2, height//2):
    D = screen.canvas_to_viewport(x, y)
    color = trace_ray(O, D, 1, np.inf)
    screen.put_pixel(x, y, color)
screen.show()
