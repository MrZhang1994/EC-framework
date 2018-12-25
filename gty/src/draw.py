import numpy
from PIL import Image, ImageDraw, ImageFont


def draw_line_v(data_p, start_p, length_p, width_p, color=[0, 0, 0]):
    data_p[start_p[0]:start_p[0]+length_p+1,
         start_p[1]: start_p[1]+width_p] = color


def draw_line_h(data_p, start_p, length_p, width_p, color=[0, 0, 0]):
    data_p[start_p[0]:start_p[0]+width_p,
         start_p[1]: start_p[1]+length_p+1] = color


def fill_color(data_p, start_p, size, color):
    for i in range(size[0]):
        line_start_p = numpy.add(start_p, [i, 0])
        draw_line_h(data_p, line_start_p, size[1], 1, color=color)
    pass


def draw_box(data_p, start_p, size):
    blw = 1  # box line width
    draw_line_h(data_p, start_p, size[1], blw)
    draw_line_h(data_p, numpy.add(start_p, [size[0], 0]), size[1], blw)

    draw_line_v(data_p, start_p, size[0], blw)
    draw_line_v(data_p, numpy.add(start_p, [0, size[1]]), size[0], blw)


def draw_text(canvas_p, start_p, string_input, color=[0, 0, 0]):
    font_size = 20
    font = ImageFont.truetype('me.ttc', font_size)  # load the font
    size = font.getsize(string_input)  # calc the size of text in pixels
    image = Image.new('1', size, 1)  # create a b/w image
    draw = ImageDraw.Draw(image)

    draw.text((0, 0), string_input, font=font)  # render the text to the bitmap
    for row_num in range(size[1]):
        for col_num in range(size[0]):
            if not image.getpixel((col_num, row_num)):
                canvas_p[start_p[0]+row_num, start_p[1]+col_num] = color


def draw_job(canvas_p,  job_name, start_p, start, end, color_filled):
    e_r = 1  # expand ratio
    box_height = 50
    box_size = [box_height, (end-start)*e_r]
    text_deviation = [10, 5]
    box_start_p = numpy.add(start_p, [0, start*e_r])
    text_start_p = numpy.add(
        numpy.add(start_p, text_deviation), [0, start*e_r])

    fill_color(canvas_p, box_start_p, box_size, color_filled)
    draw_box(canvas_p, box_start_p, box_size)
    draw_text(canvas_p, text_start_p, job_name, color=[0, 0, 0])


def draw_rule(data):
    draw_line_h(data, [90, 100], 1800, 2, [0, 0, 0])

    for i in range(10):
        de = 100 * (i)
        for j in range(2):
            draw_line_v(data, [90, 100+de+j*50], 5, 2, [0, 0, 0])

        draw_line_v(data, [90, 100+de], 10, 2, [0, 0, 0])
        draw_text(data, [60, 100+de-5], str(i), [0, 0, 0])


def draw_schedule(sche, cont, data):
    cont_color = {0: [255, 102, 102], 1: [255, 178, 102],
                  2: [255, 255, 102], 3: [178, 255, 102]}

    wr_cont = {}
    for x in cont:
        for i in range(len(sche)):
            if i in cont[x]:
                wr_cont[i] = x

    last_end = 0
    used_cpu_time = 0
    for i in range(len(sche)):
        x_processor = sche[i][3]
        x_p = 120+x_processor*100
        x_aft = sche[i][2]
        x_ast = sche[i][1]
        if (x_aft > last_end):
            last_end = x_aft
        used_cpu_time += x_aft-x_ast

        draw_job(data, str(i), [x_p, 100], int(x_ast), int(
            x_aft), color_filled=cont_color[wr_cont[i]])
        draw_text(data, [x_p+10, 20], 'core '+str(x_processor), [0, 0, 0])
        draw_line_h(data, [x_p, 100], 1800, 1, [0, 0, 0])
        draw_line_h(data, [x_p+50, 100], 1800, 1, [0, 0, 0])

    sum_cpu_time = last_end*3
    """
    for print_num in [used_cpu_time, sum_cpu_time,  used_cpu_time/sum_cpu_time]:
        print("%.2f" % print_num, end='  ')
    """

    draw_text(data, [500, 500],
              str(int(used_cpu_time/sum_cpu_time*100))+'%', [0, 0, 0])

    draw_rule(data)

    draw_line_v(data, [25, 100 + int(last_end)], int(len(data)/2) - 25*2, 1)


def draw_canvas(sche, cont,picture_name):
    size = 1024
    data = numpy.full((size, size*2, 3), 255, dtype=numpy.uint8)

    mem_data = numpy.zeros((size*2),  dtype=numpy.uint8)

    draw_schedule(sche, cont, data)

    draw_line_v(data, [25, 100], size - 25*2, 3)

    Image.fromarray(data).save(picture_name)






# # ------------1  2  3  4  5  6  7  8  9  10 11 12-----
# vertex_cpu = [3, 2, 2, 7, 7, 4, 6, 2, 7, 10, 6, 5]
# # (subtask execution)
# communication_cpu = [15.0, 16.0, 17.0, 19.0,
#                      11.0, 12.0, 15.0, 16.0, 9.0, 18.0, 10.0, 5.0]
# # (input cpu for schedule)
# arc_weight = [3, 2, 7, 6, 8, 6, 9, 5, 7, 4, 5, 4,
#               8, 6, 8, 2, 8, 4]
# # (transmission data and cpu)
# process = [13.2, 15.4, 16.5, 13.2, 4.4, 8.8, 9.9, 15.4, 2.2, 8.8, 4.4, 0.]
# # (subtask execution memory)


# for x in sche:
#     x_id = x[0]
#     if x_id == 0:
#         continue
#     x_start = x[1]
#     x_end = x[2]
#     x_container = x[3]

#     mem_middle_cut = vertex_cpu[x_id-1]

#     cpu_memory = vertex_cpu[x_id-1]

#     transmission_mem = 0
#     for x in dag[x_id]:
#         transmission_mem += arc_weight[x]

#     for i in range(int(x_end-x_start)):
#         mem_data_i = i + int(x_start)+100
#         if i < mem_middle_cut:
#             mem_data[mem_data_i] += cpu_memory
#         else:
#             mem_data[mem_data_i] += transmission_mem

# for i in range(len(mem_data)):
#     mem_data_ratio = 5
#     draw_line_v(data, [(800-mem_data[i]*mem_data_ratio), i],
#                 mem_data[i]*mem_data_ratio, 3, color=[0, 204, 204])