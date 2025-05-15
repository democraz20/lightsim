import FreeSimpleGUI as sg

import re



default_boxv = 0

def init_gui(callback_process): #implement axis keys
    labelcol1 = sg.Column([[sg.Text('position')], [sg.Text('rotaion')], [sg.Text('scale   ')]])
    inputcolx = sg.Column([[*numin(("pos", "x"))], [*numin(("rot", "x"))], [*numin(("sca", "x"))]])
    inputcoly = sg.Column([[*numin(("pos", "y"))], [*numin(("rot", "y"))], [*numin(("sca", "y"))]])
    inputcolz = sg.Column([[*numin(("pos", "z"))], [*numin(("rot", "z"))], [*numin(("sca", "z"))]])
    inccol    = sg.Column([[sg.InputText('1', key=("pos", "inc"), size=(5,0))], 
                        [sg.InputText('1', key=("rot", "inc"), size=(5,0))], 
                        [sg.InputText('1', key=("sca", "inc"), size=(5,0))]])

    layout = [[labelcol1, sg.VSeperator(), inputcolx, inputcoly, inputcolz, inccol]]

    window = sg.Window('Window Title', layout)
    event, values = window.read()

    #pos x box

    global default_boxv

    #existing box values
    last_boxv = {
        ("pos", "x") : default_boxv,
        ("rot", "y") : default_boxv,
        ("sca", "z") : default_boxv,
        ("pos", "x") : default_boxv,
        ("rot", "y") : default_boxv,
        ("sca", "z") : default_boxv,
        ("pos", "x") : default_boxv,
        ("rot", "y") : default_boxv,
        ("sca", "z") : default_boxv,
    }

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break

        elif isinstance(event, tuple) and len(event) == 3:
            #update shit , use the update button instead
            if event[2] == "box":
                #check if value was actually changed
                if not values[event] == last_boxv[(event[0], event[1])]:
                    values[event] = sanitize_input(values[event])
                    window[(event)].update(value=values[event])
                    callback_process(["gp", "pos", values[event]])
                pass
            elif event[2] == "up":
                #get value from box
                boxv = (event[0], event[1], "box")

                values[boxv] = sanitize_input(values[boxv])
                values[(event[0], "inc")] = sanitize_input(values[(event[0], "inc")])

                a = float(values[boxv]) + float(values[(event[0], "inc")])
                
                window[(boxv)].update(value=a)
                window[(event[0], "inc")].update(value=values[event[0], "inc"])

                callback_process(["gp", "pos", values[boxv]])
                pass
            elif event[2] == "down":
                pass


    window.close()

def numin(key):
    global default_boxv
    return [sg.InputText(default_boxv, key=(*key, "box"), size=(10,1), enable_events=True, pad=((10,0),0,0)),
        sg.Button('▲', key=(*key, "up"), pad=(0,1)),
        sg.Button('▼', key=(*key, "down"), pad=(0,1))]

def sanitize_input(value):
    a = ''.join(c for c in value  if c in "0123456789.")
    b = a.split(".")
    if len(b) == 1:
        return b[0]
    elif len(b) > 0:
        return b[0] + "." + "".join(b[1:])