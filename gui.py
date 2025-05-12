import FreeSimpleGUI as sg

def init_gui():
    layout = [  [sg.Text('position'), *numin("posx"), *numin("posy"), *numin("posz")],
                [sg.Text('rotation'), *numin("rotx"), *numin("roty"), *numin("rotz")],
                [sg.Text('scale   '), *numin("scax"), *numin("scay"), *numin("scaz")] ]

    window = sg.Window('Window Title', layout)
    event, values = window.read()

    window.close()

def numin(key: str):
    return [sg.InputText('0', key=f'{key}-box', size=(10,1), enable_events=True, pad=((10,0),0,0)),
        sg.Button('▲', key=f'{key}-up', pad=(0,1)),
        sg.Button('▼', key=f'{key}-down', pad=(0,1))]