def plotband(parameters):
    filedata = f"""
{parameters['prefix']}.freq
0 550
{parameters['prefix']}.xmgr
"""
    with open(f"./dyn/{parameters['prefix']}/{parameters['prefix']}-plotband.in", 'w') as file:
        file.write(filedata)
    return