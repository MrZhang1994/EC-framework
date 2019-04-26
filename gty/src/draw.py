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

def get_data_max_point(sche_input):
    max_width = 0
    for i in sche_input:
        if i[1]> max_width:
            max_width = int(i[1])
        if i[2]> max_width:
            max_width = int(i[2])
    return max_width

def get_max_from_dim(sche_in, dimention):
    result = 0
    for task in sche_in:
        if task[dimention] > result:
            result = task[dimention]
    return result

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
            if start_p[0]+row_num > len(canvas_p[0]):
                return
            if start_p[1]+col_num > len(canvas_p[1]):
                return
            #print(start_p[0]+row_num,'|',start_p[1]+col_num)
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


def draw_rule(data,max_width):
    width_factor = 5
    draw_line_h(data, [90, 100], max_width*width_factor, 2, [0, 0, 0])

    for i in range(int(max_width/100+1)):
        de = 100 * (i) * width_factor
        for j in range(2):
            draw_line_v(data, [90, 100+de+j*50*width_factor], 5, 2, [0, 0, 0])

        draw_line_v(data, [90, 100+de], 10, 2, [0, 0, 0])
        draw_text(data, [60, 100+de-5], str(i), [0, 0, 0])


def get_color_helper(x):
    # 0 < x < 875
    # sat =  saturation 
    sat = 120

    if (175 <= x < 350):
        R = (-1)*(x-175)+255
    elif (700 <= x < 700+175):
        R = (1)*(x-700)+sat
    elif (350 <= x < 700):
        R = sat
    else:
        R = 255

    if (0 <= x < 175):
        G = (1)*(x)+sat
    elif (525 <= x < 700):
        G = (-1)*(x-525)+255
    elif (175 <= x < 525):
        G = 255
    else:
        G = sat

    if (350 <= x < 525):
        B = (1)*(x-350)+sat
    elif (0 <= x < 350):
        B = sat
    else:
        B = 255

    return [int(R), int(G), int(B)]


def get_color(th, total):
    # DONE: wrap up the draw function with
    #  get_color(node_th,node_total_num)
    #  0 <= node_th <= node_total_num - 1
    # th=th+1
    #print([th, total])

    if (total == 1):
        x = 0
        return get_color_helper(x)
    else:
        x = (th)*875/(total-1)
        return get_color_helper(x)

def cal_cont_open(sche, cont):
    def cont_open_data_maintain(data_l, d_input):
        start, end = d_input

        for existed_datum in data_l:
            e_s, e_e = existed_datum

            update_code = 0
            if (e_s <= start <= end <= e_e):
                update_code = 1

            if (start <= e_s <= e_e <= end):
                update_code = 2
                existed_datum[0], existed_datum[1] = start, end

            if (e_s <= start <= e_e):
                update_code = 3
                existed_datum[1] = end

            if (e_s <= end <= e_e):
                update_code = 4
                existed_datum[0] = start

            if update_code > 0:
                return
            else:
                pass

        data_l.append(d_input)

    def cont_open_data_maintain_again(data_l):
        new_data_l = []
        for i in data_l:
            cont_open_data_maintain(new_data_l, i)
        data_l.clear()
        for i in new_data_l:
            data_l.append(i)

    cont_open_data = {}
    for cont_i in cont:
        jobs = cont[cont_i]
        for job_id in jobs:
            start = sche[job_id][1]
            end = sche[job_id][2]

            if cont_i not in cont_open_data:
                cont_open_data[cont_i] = [[start, end]]
            else:
                cont_open_data_maintain(cont_open_data[cont_i], [start, end])

            cont_open_data_maintain_again(cont_open_data[cont_i])

    result = []
    for cont_i in cont_open_data:
        job_sf = cont_open_data[cont_i]
        result.append(len(job_sf))

    return result



def draw_schedule(sche, cont, data):
    container_count = len(cont)

    core_num = get_max_from_dim(sche,3)

    cont_color = {}
    i = 0
    for color in cont:
        cont_color[i] = get_color(i, container_count)
        i += 1

    wr_cont = {}
    for x in cont:
        for i in range(len(sche)):
            if i in cont[x]:
                wr_cont[i] = x

    last_end = 0
    used_cpu_time = 0
    core_used = set()

    width_factor = 5

    gap_between_each_line = 70

    for i in range(len(sche)):
        x_processor = sche[i][3]
        x_p = 120+x_processor*gap_between_each_line
        x_aft = sche[i][2] * width_factor
        x_ast = sche[i][1] * width_factor
        if (x_aft > last_end):
            last_end = x_aft

        used_cpu_time += x_aft-x_ast

        draw_job(data, str(i), [x_p, 100], int(x_ast), int(
            x_aft), color_filled=cont_color[wr_cont[i]])

        # open a new line for a new core
        if (x_processor not in core_used):
            core_used.add(x_processor)
            draw_text(data, [x_p+10, 20], 'core '+str(x_processor), [0, 0, 0])
            draw_line_h(data, [x_p, 100], 1800, 1, [0, 0, 0])
            draw_line_h(data, [x_p+50, 100], 1800, 1, [0, 0, 0])

    sum_cpu_time = last_end*(core_num+1)

    cont_open_data = cal_cont_open(sche, cont)

    draw_text(data, [25, 300], 'con_open_times:', [0, 0, 0])

    cont_open_data_print_gap = 30

    for i in range(len(cont_open_data)):
        draw_text(data, [25, 500+i*cont_open_data_print_gap],
                  str(cont_open_data[i]), [0, 0, 0])
    #print(cont_open_data)

    # up left side
    draw_text(data, [25, 25],
              str(int(used_cpu_time/sum_cpu_time*100))+'%', [0, 0, 0])
    draw_text(data, [25, 125], 'con_num:'+str(container_count), [0, 0, 0])

    # rule
    print(get_data_max_point(sche))
    draw_rule(data,(int(get_data_max_point(sche)/100)+1)*100+30)

    # last end v line
    draw_line_v(data, [50, 100 + int(last_end)], int(len(data)) - 25*2, 1)

def get_data_span(sche_input):
    width_factor = 5
    max_width = 100
    max_core = 0
    for i in sche_input:
        if i[1]> max_width:
            max_width = int(i[1])
        if i[2]> max_width:
            max_width = int(i[2])
        if i[3]> max_core:
            max_core = i[3]

    max_width = max_width * width_factor + 150
    
    gap_between_each_line = 70
    max_height = 120 + (max_core+1)*gap_between_each_line

    return max_width,max_height


def draw_canvas(sche, cont, picture_name):
    print(sche)

    canvas_width, canvas_height = get_data_span(sche)

    data = numpy.full((canvas_height, canvas_width, 3), 255, dtype=numpy.uint8)

    #mem_data = numpy.zeros((size*2),  dtype=numpy.uint8)

    draw_schedule(sche, cont, data)

    draw_line_v(data, [90, 100], canvas_width - 25*2, 3)

    Image.fromarray(data).save(picture_name)

