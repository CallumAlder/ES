import si1145 as iig
import json

sensor = iig.SI1145()

print(sensor)
print("iig")
print("iig")
print("iig")

ir = sensor.readIR()
uv = sensor.readUV()
vis = sensor.readVisible()
# prox = sensor.readProx()

data = {"IR": ir, "UV": uv, "Visible": vis}
package = json.dumps(data)

# do another thing and then push it
# pusha T
# pushed again gg
