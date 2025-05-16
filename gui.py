import FreeSimpleGUI as sg

import re


default_boxv = 0

def init_gui(callback_process): #implement axis keys
    labelcol1 = sg.Column([[sg.Text('position')], [sg.Text('rotaion')], [sg.Text('scale   ')]])
    inputcolx = sg.Column([[*numin(("pos", "x"), default_boxv)], [*numin(("rot", "x"), default_boxv)], [*numin(("sca", "x"), 1)]])
    inputcoly = sg.Column([[*numin(("pos", "y"), default_boxv)], [*numin(("rot", "y"), default_boxv)], [*numin(("sca", "y"), 1)]])
    inputcolz = sg.Column([[*numin(("pos", "z"), default_boxv)], [*numin(("rot", "z"), default_boxv)], [*numin(("sca", "z"), 1)]])

    inccol    = sg.Column([[sg.InputText('1', key=("pos", "inc"), size=(5,0))], 
                        [sg.InputText('1', key=("rot", "inc"), size=(5,0))], 
                        [sg.InputText('1', key=("sca", "inc"), size=(5,0))]])

    layout = [[labelcol1, sg.VSeperator(), inputcolx, inputcoly, inputcolz, inccol],
             [sg.Button("update", key="updategp", expand_x=True)]]

    window = sg.Window('Control window - DO NOT CLOSE',
    layout,
    resizable=True,
    disable_close=True
    )


    #set the scale to atleast 1
    #first read just for update
    # window.read()

    # window[("sca", "x", "box")].update(value=1)
    # window[("sca", "y", "box")].update(value=1)
    # window[("sca", "z", "box")].update(value=1)


    # event, values = window.read()

    #pos x box

    # global default_boxv


    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        
        elif event == "updategp":
            #sanitize and update
            window[("pos", "x", "box")].update(value=sanitize_input(values[("pos", "x", "box")]))
            window[("pos", "y", "box")].update(value=sanitize_input(values[("pos", "y", "box")]))
            window[("pos", "z", "box")].update(value=sanitize_input(values[("pos", "z", "box")]))
            window[("rot", "x", "box")].update(value=sanitize_input(values[("rot", "x", "box")]))
            window[("rot", "y", "box")].update(value=sanitize_input(values[("rot", "y", "box")]))
            window[("rot", "z", "box")].update(value=sanitize_input(values[("rot", "z", "box")]))
            window[("sca", "x", "box")].update(value=sanitize_input(values[("sca", "x", "box")]))
            window[("sca", "y", "box")].update(value=sanitize_input(values[("sca", "y", "box")]))
            window[("sca", "z", "box")].update(value=sanitize_input(values[("sca", "z", "box")]))

            # event, values = window.read() #read once to update above calls

            l = [
                (float(values[("pos", "x", "box")]), float(values[("pos", "y", "box")]), float(values[("pos", "z", "box")])),
                (float(values[("rot", "x", "box")]), float(values[("rot", "y", "box")]), float(values[("rot", "z", "box")])),
                (float(values[("sca", "x", "box")]), float(values[("sca", "y", "box")]), float(values[("sca", "z", "box")]))
            ]
            callback_process(["gp", l])
            pass
        elif isinstance(event, tuple) and len(event) == 3:
            #update shit , use the update button instead
            if event[2] == "up":
                #get value from box
                boxv = (event[0], event[1], "box")

                values[boxv] = sanitize_input(values[boxv])
                values[(event[0], "inc")] = sanitize_input(values[(event[0], "inc")])

                a = float(values[boxv]) + float(values[(event[0], "inc")])
                
                window[(boxv)].update(value=a)
                window[(event[0], "inc")].update(value=values[event[0], "inc"])

                # callback_process(["gp", "pos", values[boxv]])
                pass
            elif event[2] == "down":
                boxv = (event[0], event[1], "box")

                values[boxv] = sanitize_input(values[boxv])
                values[(event[0], "inc")] = sanitize_input(values[(event[0], "inc")])

                a = float(values[boxv]) - float(values[(event[0], "inc")])
                window[(boxv)].update(value=a)
                window[(event[0], "inc")].update(value=values[event[0], "inc"])

                # callback_process(["gp", "pos", values[boxv]])
                pass

    window.close()
    print("stopping gui thread")

def numin(key, v):
    return [sg.InputText(v, key=(*key, "box"), size=(10,1), pad=((10,0),0,0)),
        sg.Button('▲', key=(*key, "up"), pad=(0,1)),
        sg.Button('▼', key=(*key, "down"), pad=(0,1))]

def sanitize_input(value):
    a = ''.join(c for c in value  if c in "0123456789.-")
    b = a.split(".")
    if len(b) == 1:
        return b[0]
    elif len(b) > 0:
        return b[0] + "." + "".join(b[1:])