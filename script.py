import mdl
from display import *
from matrix import *
from draw import *

def run(filename):
    """
    This function runs an mdl script
    """
    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
    else:
        print "Parsing failed."
        return

    view = [0,
            0,
            1];
    ambient = [50,
               50,
               50]
    light = [[0.5,
              0.75,
              1],
             [255,
              255,
              255]]

    color = [0, 0, 0]
    tmp = new_matrix()
    ident( tmp )

    stack = [ [x[:] for x in tmp] ]
    screen = new_screen()
    zbuffer = new_zbuffer()
    tmp = []
    step_3d = 100
    consts = ''
    coords = []
    coords1 = []
    symbols['.white'] = ['constants',
                         {'red': [0.2, 0.5, 0.5],
                          'green': [0.2, 0.5, 0.5],
                          'blue': [0.2, 0.5, 0.5]}]
    reflect = '.white'

    # print symbols
    for command in commands:
        # print(command)
        operation = command['op']
        arguments = command['args']
        if operation == "push":
            stack.append( [x[:] for x in stack[-1]] )
        elif operation == "pop":
            stack.pop()
        elif operation == "move":
            tmp = make_translate(float(arguments[0]), float(arguments[1]), float(arguments[2]))
            matrix_mult( stack[-1], tmp )
            stack[-1] = [ x[:] for x in tmp]
        elif operation == "rotate":
            theta = float(arguments[1]) * (math.pi / 180)
            if arguments[0] == 'x':
                tmp = make_rotX(theta)
            elif arguments[0] == 'y':
                tmp = make_rotY(theta)
            else:
                tmp = make_rotZ(theta)
            matrix_mult( stack[-1], tmp )
            stack[-1] = [ x[:] for x in tmp ]
        elif operation == "scale":
            tmp = make_scale(float(arguments[0]), float(arguments[1]), float(arguments[2]))
            matrix_mult( stack[-1], tmp )
            stack[-1] = [ x[:] for x in tmp]
        elif operation == "box":
            polygons = []
            add_box(polygons,
                    float(arguments[0]), float(arguments[1]), float(arguments[2]),
                    float(arguments[3]), float(arguments[4]), float(arguments[5]))
            matrix_mult( stack[-1], polygons )
            if command["constants"] != None:
                draw_polygons( polygons, screen, zbuffer, view, ambient, light, symbols, command["constants"])
            else:
                draw_polygons( polygons, screen, zbuffer, view, ambient, light, symbols, reflect)
        elif operation == "sphere":
            polygons = []
            add_sphere(polygons,
                       float(arguments[0]), float(arguments[1]), float(arguments[2]),
                       float(arguments[3]), step_3d)
            matrix_mult( stack[-1], polygons )
            if command["constants"] != None:
                draw_polygons( polygons, screen, zbuffer, view, ambient, light, symbols, command["constants"])
            else:
                draw_polygons( polygons, screen, zbuffer, view, ambient, light, symbols, reflect)
        elif operation == "torus":
            add_torus(polygons,
                      float(arguments[0]), float(arguments[1]), float(arguments[2]),
                      float(arguments[3]), float(arguments[4]), step_3d)
            matrix_mult( stack[-1], polygons )
            if command["constants"] != None:
                draw_polygons( polygons, screen, zbuffer, view, ambient, light, symbols, command["constants"])
            else:
                draw_polygons( polygons, screen, zbuffer, view, ambient, light, symbols, reflect)
        elif operation == "line":
            edges = []
            add_edge( edges,
                      float(arguments[0]), float(arguments[1]), float(arguments[2]),
                      float(arguments[3]), float(arguments[4]), float(arguments[5]) )
            matrix_mult( stack[-1], edges )
            draw_lines(edges, screen, zbuffer, color)
        elif operation == "save":
            save_extension(screen, arguments[0])
        elif operation == "display":
            display(screen)
