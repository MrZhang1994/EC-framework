import draw

sche = [(0, 0, 0, 0),
        (1, 0, 67.9, 0),
        (2, 67.9, 161.9, 0),
        (3, 161.9, 322.4, 1),
        (4, 161.9, 318.3, 0),
        (5, 460.6, 504.6, 0),
        (6, 322.4, 410.0, 2),
        (7, 318.3, 460.6, 0),
        (8, 322.4, 416.0, 1),
        (9, 504.6, 554.0, 0),
        (10, 460.6, 558.2, 1),
        (11, 416.0, 474.8, 2),
        (12, 558.2, 588.2, 0)]
cont = {0: {0, 1, 2, 3, 4}, 1: {6, 7, 8, 11}, 2: {5, 9, 10}, 3: {12}}

draw.draw_canvas(sche, cont,'a.png')

# rgbstr='aabbcc'
# print(tuple(ord(c) for c in rgbstr.decode('hex')))



a=list(bytes.fromhex("aabbcc"))

cont_color_origin = ["ff6666"];
new_cont_color = {}

i = 0
for color in cont_color_origin:
        new_cont_color[i]=list(bytes.fromhex(color))
        i+=1

print(new_cont_color)

cont_color = {0: [106, 154, 178],
                1: [123, 201, 212],
                2: [162, 227, 193],
                3: [211, 249, 175],
                4: [237, 255, 171],
                5: [255, 208, 220],
                6: [253, 227, 243],
                7: [241, 211, 255],
                8: [208, 185, 255],
                9: [171, 169, 193]}


print(a)