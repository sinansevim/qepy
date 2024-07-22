import json

def defaultConfig(path = "src/esma/configs/default.json"):
  with open(path) as f:
          data = f.read()
          config = json.loads(data)
  return config