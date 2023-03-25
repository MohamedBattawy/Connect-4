import PySimpleGUI as sg


def showtree(boardtree):
    layout = [[sg.Graph(
        canvas_size=(700,300), graph_bottom_left=(0,300), graph_top_right=(700,0),  # Define the graph area
        change_submits=True,
        key="graph",
        pad=0)]]

    window = sg.Window("Tree", layout, finalize=True)
    graph = window['graph']
    drawtree(graph,boardtree)
    i0 =0
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == "graph":  # if there's a "Graph" event, then it's a mouse movement. Move the square
            x, y = values["graph"]  # get mouse position
            id = graph.get_figures_at_location((x, y)) # this function returns the id of the figure clicked
            if len(id) > 0:
                i = int((id[0]-i0-4)/3)
                if 0 <= i < len(boardtree.neighbours) and boardtree.neighbours[i].neighbours:
                    boardtree = boardtree.neighbours[i]
                    i0 = drawtree(graph, boardtree)
    window.close()


def drawtree(graph,boardtree):
    graph.erase()
    if not boardtree.player:
        i0= graph.draw_polygon([(350, 20), (310, 100), (390, 100)], 'green')
        graph.draw_text(str(boardtree.value), (350, 70))
        for i in range(len(boardtree.neighbours)):
            graph.draw_line((350, 100), (100 * i + 50, 200))
            graph.draw_polygon([(100 * i + 10, 200), (100 * i + 90, 200), (100 * i + 50, 280)], 'red')
            if boardtree.neighbours[i].value != None:
                graph.draw_text(str(boardtree.neighbours[i].value), (100 * i + 50, 230))
            else:
                graph.draw_text("x", (100 * i + 50, 230))

    else:
        i0= graph.draw_polygon([(350, 100), (310, 20), (390, 20)], 'red')
        graph.draw_text(str(boardtree.value), (350, 50))
        for i in range(len(boardtree.neighbours)):
            graph.draw_line((350, 100), (100 * i + 50, 200))
            graph.draw_polygon([(100 * i + 10, 280), (100 * i + 90, 280), (100 * i + 50, 200)], 'green')
            if boardtree.neighbours[i].value != None:
                graph.draw_text(str(boardtree.neighbours[i].value), (100 * i + 50, 250))
            else:
                graph.draw_text("x", (100 * i + 50, 250))
    return  i0