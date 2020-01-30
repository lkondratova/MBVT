#!/usr/bin/env python
# coding: utf-8

import cv2
import csv
import os
from PIL import Image, ImageDraw, ImageColor, ImageFilter, ImageFont
from labels import area_00_108, area_01_87, area_02_108, area_02_144, area_03_76, area_03_87, area_04_76, area_04_87, area_05_76, area_05_87, area_06_53, area_07_53, area_07_76, area_08_144, area_09_53, area_09_76, area_09_87, area_10_76, area_10_87, area_11_35, area_12_53


labels_list=[area_00_108, area_01_87, area_02_108, area_02_144, area_03_76, area_03_87, area_04_76, area_04_87, 
              area_05_76, area_05_87, area_06_53, area_07_53, area_07_76, area_08_144, area_09_53, area_09_76, 
              area_09_87, area_10_76, area_10_87, area_11_35, area_12_53]
def whole_one_color():
    global cv2, csv, os, Image, ImageDraw, ImageColor, ImageFilter, ImageFont, labels_list
    #coloring each slice and saving with name from arguments (identifier).
    def color_templ(identifier, slice_no):
        identifier=str(identifier)
        slice_no = str(slice_no)
        dirpath = os.getcwd()
        out_dir = os.fsencode(dirpath) 
        for file in os.listdir(out_dir):
            filename = os.fsdecode(file)
            if filename.startswith(slice_no):
                templ1 = Image.new('RGBA', (810, 663), (255, 255, 255, 0))
                for i in range(len(labels_list)):
                    label_name=labels_list[i][0]
                    if (label_name[8:]) == slice_no+'.png':
                        area=int(label_name[5:7])
                        if colors[area] == None:
                            pass
                        else:
                            for j in range(len(labels_list[i])):
                                pixel=labels_list[i][j]
                                if type(pixel)==tuple:
                                    pixel_w=int(pixel[0])
                                    pixel_h=int(pixel[1])
                                    templ1.putpixel((pixel_w, pixel_h), colors[area])
                templ1 = templ1.filter(ImageFilter.GaussianBlur(radius=7))
                templ1.palette = None
                templ = Image.open(dirpath+'/'+slice_no+'_b0.png')
                templ.paste(templ1, (0,0), templ1)
                templ.save(str(dirpath+'/output/'+identifier+slice_no), 'PNG')
                
    # list of colors
    v1 = (0, 0, 255, 50) #1
    v2 = (0, 0, 255, 110) #2
    v3 = (0, 0, 255, 160) #3
    v4 = (0, 0, 255, 250) #4
    v5 = (0, 0, 153, 250) #5


    colormap = [0, v1, v2, v3, v4, v5]
    dirpath = os.getcwd()

    if os.path.exists(dirpath+'/output') == False:     #create an output directory where colored images will be stored
        os.makedirs(dirpath+'/output')
    #open csv file with values to be applied and color templates according to the values
    with open(dirpath+'/values.csv') as data:                 
        csv_reader = csv.reader(data, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
                pass
            else:
                values = []
                for i in range(14):
                    values.append(row[i])
                    im_name = str(values[0])
                    final_val=[]
                for i in range(13):
                    final_val.append(int((values[i+1])))
                    if float(final_val[i]) == 0:
                        final_val[i] = None
                    elif float(final_val[i]) >0 and float(final_val[i]) < 1:
                        final_val[i] = 0
                colors = []
                for i in range(len(final_val)):
                    if final_val[i] == None:
                        colors.append(None)
                    else:
                        colors.append(colormap[int(final_val[i])])
                color_templ(im_name, 35)
                color_templ(im_name, 53)
                color_templ(im_name, 76)
                color_templ(im_name, 87)
                color_templ(im_name, 108)
                color_templ(im_name, 144)
    #put images from output folder in row 6 by 6 (where each 6 pictures represent data for one sample) 
    #save in 'pdf' folder

    if os.path.exists(dirpath+'/output/pdf') == False:
        os.makedirs(dirpath+'/output/pdf')
    with open(dirpath+'/values.csv') as data:
        csv_reader = csv.reader(data, delimiter=',')
        line_count = 0
        values = []
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
                pass
            else:
                values.append(row[0])
    for i in range(len(values)):
        background = Image.new('RGBA', (1620, 221), (255, 0, 0, 0))
        out_dir = os.fsencode(dirpath+'/output')
        for file in os.listdir(out_dir):
            filename = os.fsdecode(file)
            new_name=values[i][0:(len(values[i]))]
            if filename.startswith(new_name):
                im = Image.open(dirpath+'/output/'+filename)
                im.palette = None
                resized_filename=im.resize((270,221), Image.LANCZOS)
                if filename.endswith('35'):
                    background.paste(resized_filename, (0,0))
                elif filename.endswith('53'):
                    background.paste(resized_filename, (270,0))
                elif filename.endswith('76'):
                    background.paste(resized_filename, (540,0))
                elif filename.endswith('87'):
                    background.paste(resized_filename, (810,0))
                elif filename.endswith('108'):
                    background.paste(resized_filename, (1080,0))
                elif filename.endswith('144'):
                    background.paste(resized_filename, (1350,0))
        background.save(dirpath+'/output/pdf/'+new_name+'.png', 'PNG')
    #save all pictures from pdf folder in .pdf file
    pdf_file = dirpath+'/output/pdf/whole_one_colored.pdf'
    out_dir = os.fsencode(dirpath+'/output/pdf')
    images = []
    font = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 40)
    font1 = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 30)
    files = os.listdir(out_dir)
    for file in sorted(files):
        filename = os.fsdecode(file)
        if filename.endswith(".png"):
            filename1 = filename[0:(len(filename)-4)]          #this is the legend name which coresponds to the name in values.csv file.
            im = Image.open(dirpath+'/output/pdf'+'/'+filename)
            img = Image.new('RGB', (1620, 221), '#1a1a1a')
            img.paste(im, (0,0), mask=im)
            draw = ImageDraw.Draw(img)
            draw.text((10, 180), filename1, fill='#FFFFFF', font=font1)
            images.append(img)
    images[0].save(pdf_file, save_all=True, append_images=images[1:])
    if os.path.exists(dirpath+'/output/pdf/whole_one_colored.pdf') == True:
        return ("file 'whole_one_colored.pdf' saved in an 'output/pdf' folder")
    else:
        return ('something went wrong!')
    



def whole_colorscale():
    global cv2, csv, os, Image, ImageDraw, ImageColor, ImageFilter, ImageFont, labels_list
    # this block is for coloring each slice and saving with name from arguments using lables saved as python list
    def color_templ(out_name, slice_no):
        out_name=str(out_name)
        slice_no = str(slice_no)
        dirpath = os.getcwd()
        out_dir = os.fsencode(dirpath) 
        for file in os.listdir(out_dir):
            filename = os.fsdecode(file)
            if filename.startswith(slice_no):
                templ = Image.open(dirpath+'/'+filename)
                for i in range(len(labels_list)):
                    label_name=labels_list[i][0]
                    if (label_name[8:]) == slice_no+'.png':
                        area=int(label_name[5:7])
                        if colors[area] == None:
                            pass
                        else:
                            for j in range(len(labels_list[i])):
                                pixel=labels_list[i][j]
                                if type(pixel)==tuple:
                                    pixel_w=int(pixel[0])
                                    pixel_h=int(pixel[1])
                                    templ.putpixel((pixel_w, pixel_h), ImageColor.getcolor(colors[area],'RGBA'))
                templ = templ.filter(ImageFilter.BLUR)
                templ.save(str(dirpath+'/output/'+out_name+'_'+slice_no), 'PNG')

    # list of colors
    dark_blue = '#0000FF'
    blue = '#00CED1'
    yellow = '#EEC900'
    orange = '#FFA500'
    red = '#FF4500'
    dark_red = '#8B2500'

    colormap = [dark_blue, blue, yellow, orange, red, dark_red]
    dirpath = os.getcwd()

    if os.path.exists(dirpath+'/output') == False:
        os.makedirs(dirpath+'/output')

    with open(dirpath+'/values.csv') as data:
        csv_reader = csv.reader(data, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
                pass
            else:
                values = []
                for i in range(14):
                    values.append(row[i])
                    im_name = str(values[0])
                    final_val=[]
                for i in range(13):
                    final_val.append(values[i+1])
                for i in range(13):
                    if float(final_val[i]) == 0:
                        final_val[i] = None
                    elif float(final_val[i]) >0 and float(final_val[i]) < 1:
                        final_val[i] = 0
                colors = []
                for i in range(len(final_val)):
                    if final_val[i] == None:
                        colors.append(None)
                    else:
                        colors.append(colormap[int(final_val[i])])
                color_templ(im_name, 35)
                color_templ(im_name, 53)
                color_templ(im_name, 76)
                color_templ(im_name, 87)
                color_templ(im_name, 108)
                color_templ(im_name, 144)

    #create picture explaining colormap
    colorscale = Image.new('RGB', (100, 40), '#FFFFFF')
    font = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 25)
    draw = ImageDraw.Draw(colorscale)
    draw.text((3, 0), '1', fill='#000000', font=font)
    draw.text((85, 0), '5', fill='#000000', font=font)
    for i in range(100):
        for j in range(40):
            if i<=20 and j>20:
                colorscale.putpixel((i, j), ImageColor.getcolor(colormap[1],'RGB'))
            elif i>20 and i<=40 and j>20:
                colorscale.putpixel((i, j), ImageColor.getcolor(colormap[2],'RGB'))
            elif i>40 and i<=60 and j>20:
                colorscale.putpixel((i, j), ImageColor.getcolor(colormap[3],'RGB'))
            elif i>60 and i<=80 and j>20:
                colorscale.putpixel((i, j), ImageColor.getcolor(colormap[4],'RGB'))
            elif i>80 and i<=100 and j>20:
                colorscale.putpixel((i, j), ImageColor.getcolor(colormap[5],'RGB'))
        colorscale.mode = 'RGBA'
        colorscale.save(str(dirpath+'/output/colorscale'), 'PNG')
        
    if os.path.exists(dirpath+'/output/pdf') == False:
        os.makedirs(dirpath+'/output/pdf')
    
    #put images in row by 6 and save in 'pdf' folder
    with open(dirpath+'/values.csv') as data:
        csv_reader = csv.reader(data, delimiter=',')
        line_count = 0
        values = []
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
                pass
            else:
                values.append(row[0])
    for i in range(len(values)):
        background = Image.new('RGBA', (1620, 221), (255, 0, 0, 0))
        out_dir = os.fsencode(dirpath+'/output')
        x_offset = 0
        for file in os.listdir(out_dir):
            filename = os.fsdecode(file)
            if filename.startswith(values[i]):
                im = Image.open(dirpath+'/output/'+filename)
                im.palette = None
                resized_filename=im.resize((270,221), Image.LANCZOS)
                if filename.endswith('35'):
                    background.paste(resized_filename, (0,0))
                elif filename.endswith('53'):
                    background.paste(resized_filename, (270,0))
                elif filename.endswith('76'):
                    background.paste(resized_filename, (540,0))
                elif filename.endswith('87'):
                    background.paste(resized_filename, (810,0))
                elif filename.endswith('108'):
                    background.paste(resized_filename, (1080,0))
                elif filename.endswith('144'):
                    background.paste(resized_filename, (1350,0))
        scale = Image.open((dirpath+'/output/colorscale'))
        background.paste(scale, (1450,180))
        background.save(dirpath+'/output/pdf/'+values[i]+'.png', 'PNG')
        
    
    
    pdf_file = dirpath+'/output/pdf/whole_colorscale.pdf'
    out_f = os.fsencode(dirpath+'/output/pdf')
    images = []
    font = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 40)
    files = os.listdir(out_f)
    for file in sorted(files):
        filename = os.fsdecode(file)
        if filename.endswith(".png"):
            filename1 = filename[0:(len(filename)-8)]
            im = Image.open(dirpath+'/output/pdf'+'/'+filename)
            img = Image.new('RGB', (1620, 221), '#FFFFFF')
            img.paste(im, (0,0), mask=im)
            draw = ImageDraw.Draw(img)
            draw.text((0, 180), filename1, fill='#000000', font=font)
            images.append(img)
    images[0].save(pdf_file, save_all=True, append_images=images[1:])
    if os.path.exists(dirpath+'/output/pdf/whole_colorscale.pdf') == True:
        return ("file 'whole_colorscale.pdf' saved in an 'output/pdf' folder")
    else:
        return ('something went wrong!')
    


def two_sided_colorscale():
    global cv2, csv, os, Image, ImageDraw, ImageColor, ImageFilter, ImageFont, labels_list 
    
    dirpath = os.getcwd()
    def color_left(identifier, slice_no):
        identifier=str(identifier)
        slice_no = str(slice_no)
        dirpath = os.getcwd()
        out_dir = os.fsencode(dirpath) 
        for file in os.listdir(out_dir):
            filename = os.fsdecode(file)
            if filename.startswith(slice_no):
                templ = Image.open(dirpath+'/'+filename)
                for i in range(len(labels_list)):
                    label_name=labels_list[i][0]
                    if (label_name[8:]) == slice_no+'.png':
                        area=int(label_name[5:7])
                        if colors[area] == None:
                            pass
                        else:
                            for j in range(len(labels_list[i])):
                                pixel=labels_list[i][j]
                                if type(pixel)==tuple:
                                    pixel_w=int(pixel[0])
                                    pixel_h=int(pixel[1])
                                    if pixel_w < 394:
                                        templ.putpixel((pixel_w, pixel_h), ImageColor.getcolor(colors[area],'RGBA'))
                templ.save(str(dirpath+'/output/left_part/'+identifier+slice_no), 'PNG')


    def color_right(identifier, slice_no):
        identifier=str(identifier)
        slice_no = str(slice_no)
        dirpath = os.getcwd()
        out_dir = os.fsencode(dirpath+'/output/left_part') 
        for file in os.listdir(out_dir):
            filename = os.fsdecode(file)
            if filename.endswith(slice_no) and filename.startswith(identifier):
                templ = Image.open(dirpath+'/output/left_part/'+filename)
                for i in range(len(labels_list)):
                    label_name=labels_list[i][0]
                    if (label_name[8:]) == slice_no+'.png':
                        area=int(label_name[5:7])
                        if colors[area] == None:
                            pass
                        else:
                            for j in range(len(labels_list[i])):
                                pixel=labels_list[i][j]
                                if type(pixel)==tuple:
                                    pixel_w=int(pixel[0])
                                    pixel_h=int(pixel[1])
                                    if pixel_w > 394:
                                        templ.putpixel((pixel_w, pixel_h), ImageColor.getcolor(colors[area],'RGBA'))
                templ = templ.filter(ImageFilter.BLUR)
                templ.save(str(dirpath+'/output/'+identifier+slice_no), 'PNG')
                os.remove(dirpath+'/output/left_part/'+filename)

        
        # list of colors
    v1 = '#6495ED' #1
    v2 = '#BCD2EE' #2
    v3 = '#FFE4E1' #3
    v4 = '#F08080' #4
    v5 = '#FF4040' #5

    colormap = [0, v1, v2, v3, v4, v5]

    if os.path.exists(dirpath+'/output') == False:
        os.makedirs(dirpath+'/output')
    if os.path.exists(dirpath+'/output/left_part') == False:
        os.makedirs(dirpath+'/output/left_part')

    with open(dirpath+'/values.csv') as data:
        csv_reader = csv.reader(data, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
                pass
            else:
                values = []
                for i in range(14):
                    values.append(row[i])
                    im_name = str(values[0])
                    final_val=[]
                for i in range(13):
                    final_val.append(values[i+1])
                for i in range(13):
                    if float(final_val[i]) == 0:
                        final_val[i] = None
                    elif float(final_val[i]) >0 and float(final_val[i]) < 1:
                        final_val[i] = 1
                colors = []
                for i in range(len(final_val)):
                    if final_val[i] == None:
                        colors.append(None)
                    else:
                        colors.append(colormap[int(final_val[i])])
                if im_name.endswith('dna'):
                    im_name1 = im_name[0:(len(im_name)-3)]
                    color_left(im_name1, 35)
                    color_left(im_name1, 53)
                    color_left(im_name1, 76)
                    color_left(im_name1, 87)
                    color_left(im_name1, 108)
                    color_left(im_name1, 144)
                if im_name.endswith('rna'):
                    im_name2 = im_name[0:(len(im_name)-3)]
                    color_right(im_name2, 35)
                    color_right(im_name2, 53)
                    color_right(im_name2, 76)
                    color_right(im_name2, 87)
                    color_right(im_name2, 108)
                    color_right(im_name2, 144)
    
    if len(os.listdir(dirpath+'/output/left_part')) == 0:
        os.rmdir(dirpath+'/output/left_part')
    else:    
        print("Error: Make sure each _DNA ending sample name has corresponding _RNA ending name.")
                
    #create picture explaining colormap               
    colorscale = Image.new('RGB', (75, 25), '#FFFFFF')
    font = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 13)
    draw = ImageDraw.Draw(colorscale)
    draw.text((3, 0), '1', fill='#000000', font=font)
    draw.text((65, 0), '5', fill='#000000', font=font)
    for i in range(75):
        for j in range(25):
            if i<=15 and j>10:
                colorscale.putpixel((i, j), ImageColor.getcolor(colormap[1],'RGB'))
            elif i>15 and i<=30 and j>10:
                colorscale.putpixel((i, j), ImageColor.getcolor(colormap[2],'RGB'))
            elif i>30 and i<=45 and j>10:
                colorscale.putpixel((i, j), ImageColor.getcolor(colormap[3],'RGB'))
            elif i>45 and i<=60 and j>10:
                colorscale.putpixel((i, j), ImageColor.getcolor(colormap[4],'RGB'))
            elif i>60 and i<=75 and j>10:
                colorscale.putpixel((i, j), ImageColor.getcolor(colormap[5],'RGB'))
    colorscale.mode = 'RGBA'
    colorscale.save(str(dirpath+'/output/colorscale'), 'PNG')

    if os.path.exists(dirpath+'/output/pdf') == False:
        os.makedirs(dirpath+'/output/pdf')
    with open(dirpath+'/values.csv') as data:
        csv_reader = csv.reader(data, delimiter=',')
        line_count = 0
        values = []
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
                pass
            else:
                values.append(row[0])
    for i in range(len(values)):
        background = Image.new('RGBA', (1620, 221), (255, 0, 0, 0))
        out_f = os.fsencode(dirpath+'/output')
        for file in os.listdir(out_f):
            filename = os.fsdecode(file)
            new_name=values[i][0:(len(values[i])-4)]
            if filename.startswith(new_name):
                im = Image.open(dirpath+'/output/'+filename)
                im.palette = None
                resized_filename=im.resize((270,221), Image.LANCZOS)
                if filename.endswith('35'):
                    background.paste(resized_filename, (0,0))
                elif filename.endswith('53'):
                    background.paste(resized_filename, (270,0))
                elif filename.endswith('76'):
                    background.paste(resized_filename, (540,0))
                elif filename.endswith('87'):
                    background.paste(resized_filename, (810,0))
                elif filename.endswith('108'):
                    background.paste(resized_filename, (1080,0))
                elif filename.endswith('144'):
                    background.paste(resized_filename, (1350,0))
        scale = Image.open((dirpath+'/output/colorscale'))
        background.paste(scale, (1500,195))
        background.save(dirpath+'/output/pdf/'+new_name+'.png', 'PNG')
        
        
    #save all pictures from pdf folder in .pdf file
    import os
    from PIL import Image, ImageDraw, ImageFont

    dirpath = os.getcwd()
    pdf_file = dirpath+'/output/pdf/two_sided_colorscale.pdf'
    out_dir = os.fsencode(dirpath+'/output/pdf')
    images = []
    font = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 40)
    files = os.listdir(out_dir)
    for file in sorted(files):
        filename = os.fsdecode(file)
        if filename.endswith(".png"):
            filename1 = filename[0:(len(filename)-4)]
            im = Image.open(dirpath+'/output/pdf'+'/'+filename)
            img = Image.new('RGB', (1620, 221), '#282828')
            img.paste(im, (0,0), mask=im)
            draw = ImageDraw.Draw(img)
            draw.text((0, 180), filename1, fill='#FFFFFF', font=font)
            draw.text((5, 5), 'DNA', fill='#FFFFFF', font=font)
            draw.text((190, 5), 'RNA', fill='#FFFFFF', font=font)
            images.append(img)
    images[0].save(pdf_file, save_all=True, append_images=images[1:])
    if os.path.exists(dirpath+'/output/pdf/two_sided_colorscale.pdf') == True:
        return ("file 'two_sided_colorscale.pdf' saved in an 'output/pdf' folder")
    else:
        return ('something went wrong!')
    
    
execute = input("Enter the command (whole_one_color(), whole_colorscale() or two_sided_colorscale()):\n")
if execute == 'whole_one_color()':
    whole_one_color()
elif execute == 'whole_colorscale()':
    whole_colorscale()
elif execute == 'two_sided_colorscale()':
    two_sided_colorscale()
elif len(execute) == 0:
    print ("You did not enter the function name")
else:
    print ("Function name is not correct")
        

