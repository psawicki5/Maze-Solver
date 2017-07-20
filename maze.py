from PIL import Image

im = Image.open('maze_2.gif')


pixels = list(im.getdata())
width, height = im.size


# getting pixels in tables
pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]


def print_pixels(pixels):
    """
    Prints nested arrays as a matrix
    :param pixels nested arrays - matrix that represents maze
    """
    height = len(pixels)
    width = len(pixels[0])
    for i in range(height):
        for j in range(width):
            print(pixels[i][j], end=" ")
        print()


class Node(object):
    id = 0

    def __init__(self, row, column):
        self.row = row
        self.column = column
        self.id = Node.id
        self.previous_node = None
        self.distance_to_node = 999999
        Node.id += 1

    def __str__(self):
        return "N" + str(self.id)


# cuts white borders around maze
pixels.pop()
pixels.pop(0)
for row in pixels:
    row.pop(0)
    row.pop()


def find_start_stop(pixels):
    """
    Finds start/end nodes
    :param pixels: list - list of pixels
    :return: list- list with start/end nodes
    """
    n_width = len(pixels[0])
    n_height = len(pixels)
    node_list = []
    for i in range(0, n_height):
        for j in range(0, n_width):
            current = pixels[i][j]
            if current == 0 and (i in (0, n_height - 1) or j in (0, n_width - 1)):
                node = Node(i, j)
                if node_list:
                    node.end = True
                else:
                    node.start = True
                node_list.append(node)
    return node_list


def find_nodes(pixels):
    """
    Find nodes in maze(finds crossections)
    :param pixels: list - nested list of pixels representing nodes
    :return: list - list of pixels
    """
    n_width = len(pixels[0])
    n_height = len(pixels)
    node_list = []
    for i in range(1, n_height - 1):
        for j in range(1, n_width - 1):
            current = pixels[i][j]
            high = pixels[i + 1][j]
            low = pixels[i - 1][j]
            left = pixels[i][j - 1]
            right = pixels[i][j + 1]

            if not current:
                if ((high == 0 and right == 0) or (high == 0 and left == 0) or
                        (low == 0 and right == 0) or (low == 0 and left == 0)):
                    node = Node(i, j)
                    node_list.append(node)
                if ((high and right and left) or (low and right and left) or
                        (high and low and left) or (high and low and right)):
                    node = Node(i, j)
                    node_list.append(node)
    return node_list


def append_nodes_to_pixels(pixels, node_list):
    """
    Appends nodes to pixel image
    :param pixels: list - list of pixels
    :param node_list: list - list of nodes
    :return: list - list of pixels with appended nodes in their proper locations
    """
    for node in node_list:
        pixels[node.row][node.column] = node
    return pixels


def check_top(node, pixels_nodes, n_height, matrix):
    """
    Checks if on the top of current node is another node and mesaures distance
    to it
    :param node: Node class object
    :param pixels_nodes: list - list of nodes
    :param n_width: int - width of matrix
    :param n_height: int - height of matrix
    :param matrix: nested lists - matrix representing nodes neighborhood
    :return: matrix with appended distance to node on the top
    """
    row = node.row + 1
    column = node.column
    distance = 1
    while row < n_height:
        if type(pixels_nodes[row][column]) == Node:
            next_node = pixels_nodes[row][column]
            matrix[node.id][next_node.id] = distance
            break
        elif pixels_nodes[row][column] == 1:
            break
        row += 1
        distance += 1

    return matrix


def check_bottom(node, pixels_nodes, matrix):
    """
    The same as in check_top...
    """
    row = node.row - 1
    column = node.column
    distance = 1
    while row >= 0:
        if type(pixels_nodes[row][column]) == Node:
            next_node = pixels_nodes[row][column]
            matrix[node.id][next_node.id] = distance
            break
        elif pixels_nodes[row][column] == 1:
            break
        row -= 1
        distance += 1
    return matrix


def check_right(node, pixels_nodes, n_width, matrix):
    """
    The same as in check_top...
    """
    row = node.row
    column = node.column + 1
    distance = 1
    while column < n_width:
        if type(pixels_nodes[row][column]) == Node:
            next_node = pixels_nodes[row][column]
            matrix[node.id][next_node.id] = distance
            break
        elif pixels_nodes[row][column] == 1:
            break
        column += 1
        distance += 1
    return matrix


def check_left(node, pixels_nodes, matrix):
    """
    The same as in check_top...
    """
    row = node.row
    column = node.column - 1
    distance = 1
    while column >= 0:
        if type(pixels_nodes[row][column]) == Node:
            next_node = pixels_nodes[row][column]
            matrix[node.id][next_node.id] = distance
            break
        elif pixels_nodes[row][column] == 1:
            break
        column -= 1
        distance += 1
    return matrix


def check_neighbours(node, pixels_nodes, n_width, n_height, matrix):
    """
    Checks for neighbouring nodes and saves them to relation matrix
    :param node: Node object - current node that we are in
    :param pixels_nodes: nested list - table with maze and appended nodes
    :param n_width: int - width of maze
    :param n_height: int - height of maze
    :param matrix: matrix - matrix of relations between nodes
    :return: matrix with filled relations for current node
    """
    matrix = check_top(node, pixels_nodes, n_height, matrix)
    matrix = check_bottom(node, pixels_nodes, matrix)
    matrix = check_right(node, pixels_nodes, n_width, matrix)
    matrix = check_left(node, pixels_nodes, matrix)
    return matrix


def create_matrix(pixels_nodes, node_list):
    """
    Creates matrix with maze and appended nodes
    :param pixels_nodes: nested list - table with maze and appended nodes
    :param node_list: list - list of all nodes in maze
    :return: matrix with filled relations for all nodes
    """
    n_width = len(pixels[0])
    n_height = len(pixels)
    matrix = []
    for i in range(len(node_list)):
        matrix_row = []
        for j in range(len(node_list)):
            matrix_row.append(0)
        matrix.append(matrix_row)
    for node in node_list:
        matrix = check_neighbours(node, pixels_nodes, n_width, n_height, matrix)
    return matrix


def pop_node(min_node_id, available_nodes):
    """
    Removes visited node from available nodes list
    :param min_node_id: int - id of visited node
    :param available_nodes: list - list of available nodes
    :return: list - list of available nodes
    """
    for key, node in enumerate(available_nodes):
        if node.id == min_node_id:
            available_nodes.pop(key)
    return available_nodes


def get_adj_nodes(available_nodes, calculation_nodes, n_matrix, current_node):
    """
    Gets all adjacent and available nodes to current node
    :param available_nodes: list - list of available nodes
    :param n_matrix: nested lists - matrix with relations of nodes
    :param current_node: VisitedNode class object
    :return: list - list of adjacent nodes
    """
    row = n_matrix[current_node.id]
    adj_nodes = []
    for key, distance in enumerate(row):
        if distance:
            node = calculation_nodes[key]
            if node in available_nodes:
                adj_nodes.append(node)
    return adj_nodes


def get_min_node(current_node, n_matrix, visited_nodes, calculation_nodes):
    """
    Returns node with minimum distance to start node
    :param current_node: Calculation Node object
    :param n_matrix: matrix - relation matrix
    :param visited_nodes: list - list with visited nodes
    :param calculation_nodes:list - list of all calculation nodes
    :return: Calculation node object with shortest distance to start node
    """
    row = n_matrix[current_node.id]
    current_calculation_node_list = []

    for node_id, distance in enumerate(row):
        if distance and calculation_nodes[node_id] not in visited_nodes:
            node = calculation_nodes[node_id]
            node.previous_node = current_node
            node.distance_to_node = \
                node.previous_node.distance_to_node + distance
            current_calculation_node_list.append(node)
    try:
        min_node = min(current_calculation_node_list,
                       key=lambda n: n.distance_to_node)
    except ValueError:
        min_node = current_node.previous_node
    return min_node


def dikstras_alghorithm(n_matrix, node_list):
    """
    Implements alghorithm of search for quickest path
    :param n_matrix: nested lists - matrix with relations of nodes
    :param node_list: list - list of all nodes in maze
    :return: node at the end of path
    """
    start_node_id = 0
    stop_node_id = 1

    calculation_nodes = node_list
    # setting start node distance 0
    calculation_nodes[0].distance_to_node = 0

    available_nodes = [node for node in calculation_nodes]
    # removes start node from available nodes
    start_node = available_nodes.pop(0)

    visited_nodes = [start_node]
    current_node = start_node

    while current_node.id != stop_node_id:
        # gets closest node to current node
        min_node = get_min_node(current_node, n_matrix,
                                visited_nodes, calculation_nodes)

        current_node = min_node
        # Relax
        # gets all adjacent and available nodes to current node
        adj_nodes = get_adj_nodes(available_nodes, calculation_nodes,
                                  n_matrix, current_node)
        # check if there is shorter path than current shortest path
        for node in adj_nodes:
            # if there is shorter path then now it is current path
            if node.distance_to_node < current_node.distance_to_node:
                current_node = node
        visited_nodes.append(current_node)
        available_nodes = pop_node(current_node.id, available_nodes)
    # returns node at the end of maze
    return current_node


def print_line(node_1, node_2, image):
    """
    Prints red lines between nodes
    :param node_1: VisitedNode object
    :param node_2: VisitedNode object
    :param image: image as RGB
    :param node_list: list - list of all nodes in maze
    :return: image with red lines between visited two nodes
    """
    x1 = node_1.column
    y1 = node_1.row

    x2 = node_2.column
    y2 = node_2.row

    if y1 == y2:
        if x2 < x1:
            x1, x2 = x2, x1
        for i in range(x1, x2 + 1):
            image.putpixel((i + 1, y1 + 1), (255, 0, 0))
    elif x1 == x2:
        if y2 < y1:
            y1, y2 = y2, y1
        for j in range(y1, y2 + 1):
            image.putpixel((x1 + 1, j + 1), (255, 0, 0))
    return image


def print_path(node, im):
    """
    Prints path from start to the end of maze
    :param node: VisitedNode - node at the end of maze
    :param im: image of maze
    :param node_list: list - list of all nodes in maze
    :return: image with printed red lines between all nodes
    """
    new_image = im.convert('RGB')

    while(node):
        back_node = node
        node = node.previous_node
        if back_node and node:
            new_image = print_line(back_node, node, new_image)
    return new_image

# makes node list
node_list = find_start_stop(pixels) + find_nodes(pixels)
print("Nodes number: ", len(node_list))

# appends nodes to pixels
pixels_nodes = append_nodes_to_pixels(pixels, node_list)
print("Nodes appended to picture")

# creates matrix of relations between nodes
matrix = create_matrix(pixels, node_list)
print("Relation matrix created")

# returns node that is at the end of maze
current_node = dikstras_alghorithm(matrix, node_list)
print("Path calculated")

# prints path lenght
print("Path length:", current_node.distance_to_node)

# tracks down nodes from end to start and paints paths between them
new_image = print_path(current_node, im)
# saves output as new image
new_image.save('out.bmp')
print("Image saved !!!")

