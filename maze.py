from PIL import Image, ImageFilter

im = Image.open('maze.gif')
'''if im.mode != 'RGBA':
    im = im.convert('RGBA')'''

pixels = list(im.getdata())
width, height = im.size


# getting pixels in tables
pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]


def print_pixels(pixels):
    height = len(pixels)
    width = len(pixels[0])
    for i in range(height):
        for j in range(width):
            print(pixels[i][j], end=" ")
        print("jjhjhhg")

#im.show()


class Node(object):
    id = 1

    def __init__(self, row, column):
        self.row = row
        self.column = column
        self.id = Node.id
        self.end = False
        self.start = False
        Node.id += 1

    def __str__(self):
        return "N" + str(self.id)


pixels.pop()
pixels.pop(0)
for row in pixels:
    row.pop(0)
    row.pop()


# Find Nodes
def find_nodes(pixels):
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
                    pixels[i][j] = node

    return pixels, node_list


for j in range(len(pixels[0])):
    pass



print_pixels(pixels)
print()
new_pixels, node_list = find_nodes(pixels)
print_pixels(new_pixels)
print(*node_list)
