import datetime as t
import os
from dataclasses import dataclass
import typing as ty



@dataclass
class BalloonState:
  date_time: t.datetime
  lat: float
  long: float
  alt: float
  vert_speed: float

@dataclass
class GramGrid:
  lat: ty.List[float]
  long: ty.List[float]
  alt: ty.List[float]

"""with open('output.txt', newline = '') as f:
	output_txt = f.readlines()

x = [0,1,2,3]

temp = []

alt = []
lat = []
long = []
p = []
rho = []
temperature = []
wind_E = []
wind_N = []
wind_Z = []

for i in range(len(output_txt)):
  if "Positions generated" in output_txt[i]:
    start_line = i + 2
    break
  else:
    start_line = 35

for i in x:
  temp = output_txt[start_line + 13*i].split()
  
  print(temp[5])

  alt.append(temp[0])
  lat.append(temp[1])
  long.append(temp[2])
  p.append(temp[3])
  rho.append(temp[4])
  temperature.append(temp[5])
  wind_E.append(temp[6])
  wind_N.append(temp[7])
  wind_Z.append(temp[8])

print(wind_Z)"""