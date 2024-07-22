import json


def generic(self):
    with open(self.file_path, 'w') as file:
        for i,j in self.config[self.package].items():
            if i!='hubbard':
                try:
                    if(type(j)==dict):
                            file.write(f"&{i.upper()} \n")
                    for k,l in j.items():
                        try:
                            float(l)
                            file.write(f"{k} = {l} \n")
                        except:
                            try:
                                json.loads(l)
                                file.write(f"{k} = .{l}. \n")
                            except:
                                if(bool(l)):
                                    file.write(f"{k} = '{l}' \n")
                    file.write("/ \n")
                except:
                    pass