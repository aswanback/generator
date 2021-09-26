import os
import random
import helper as h
from PIL import Image, ImageFont, ImageDraw

# Generate one target and save to file
def generateTarget(filepath:str,shape:str,shape_color:tuple,shape_size:int,alphanumeric:str,alpha_color:tuple,font_size:int,resize_ratio:float = 1.05, bkgd_format:str='png'):
    draw_funcs = [h.circle, h.semicircle, h.quartercircle, h.triangle, h.square, h.rectangle,h.trapezoid, h.pentagon, h.hexagon, h.heptagon, h.octagon, h.star, h.cross]
    shape_func = draw_funcs[h.Shape.index(shape)]
    font = ImageFont.truetype("Helvetica.ttf", font_size)
    center = (int(shape_size / 2), int(shape_size / 2))  # set center at center of img

    bkgd_alpha = 0
    if bkgd_format == 'png':
        bkgd_alpha = 0
    elif bkgd_format == 'jpg':
        bkgd_alpha = 255

    # shape
    im = Image.new('RGBA', (shape_size, shape_size), (0,0,0,bkgd_alpha))
    draw = ImageDraw.Draw(im)
    shape_func(draw,shape_color,shape_size/resize_ratio,center)

    # text
    text_w, text_h = draw.textsize(alphanumeric, font=font)  # get text size
    txt = Image.new('RGBA',(text_w*2,text_h*2),(0,0,0,0))
    d = ImageDraw.Draw(txt)
    d.text((text_w/2,text_h/2), alphanumeric, alpha_color, font=font)
    txt = txt.rotate(random.randint(0,360),expand=0,fillcolor=(0,0,0,0)) # random angle rotation

    # combine
    im.paste(txt,(center[0]-text_w,center[1]-text_h),txt)
    im.save(filepath)

# generate a bunch of targets and save to file
def generateTargetDataset(target_dir:str,num_each:int,shape_size:int,font_size:int,clear_dir=False,bkgd_format='png'):
    if target_dir in os.listdir() and clear_dir: os.system(f'rm -rf {target_dir}')
    if target_dir not in os.listdir(): os.mkdir(target_dir)

    for _ in range(num_each):
        for shape_idx in range(len(h.Shape)):
            # Grab random indices
            alnum_idx = random.randint(0,len(h.Alphanumeric)-1)

            color_idx_al = random.randint(0,len(h.Color)-1)
            color_idx_sh = random.randint(0, len(h.Color)-1)
            while color_idx_sh == color_idx_al:
                color_idx_sh = random.randint(0,len(h.Color)-1)

            # get params based on indices
            alnum = h.Alphanumeric[alnum_idx]
            shape = h.Shape[shape_idx]
            color_al = h.Color[color_idx_al]
            color_sh = h.Color[color_idx_sh]

            color_al_rgba = h.getRandomRGBA(color_idx_al)
            color_sh_rgba = h.getRandomRGBA(color_idx_sh)

            # make target
            i = 0
            filename = target_dir + '/' + '-'.join([shape.lower(), color_sh.lower(), alnum.lower(), color_al.lower(),str(i)]) +'.png'
            while filename in os.listdir():
                filename = filename[:-5] + str(i) + '.png'
                i += 1
            generateTarget(filename,shape,color_sh_rgba,shape_size,alnum,color_al_rgba,font_size,bkgd_format=bkgd_format)

# generate a training image based on stored files
def generateImgAndTxt(outfilename:str, shape_dir:str, bkgd_dir:str,num_targets:int,seamless=False):

    bkgd_img_filenames = os.listdir(bkgd_dir)
    bkgd_fp = random.choice(bkgd_img_filenames)
    bkgd = Image.open(bkgd_dir+'/'+bkgd_fp, 'r')
    b_w, b_h = bkgd.size
    bkgd.close()

    shape_img_filenames = os.listdir(shape_dir)
    shape_fps = random.sample(shape_img_filenames,num_targets)
    shapes = [Image.open(shape_dir+'/'+f) for f in shape_fps]
    shape_names = [s.split('-')[0] for s in shape_fps]
    shape_nums = [h.Shape.index(s.upper()) for s in shape_names]
    shape_sizes = [s.size for s in shapes]
    for s in shapes:
        s.close()

    # out = Image.new('RGBA',bkgd.size)
    # out.paste(bkgd)

    locations = []
    bbox = []
    for shape_num,shape_size in zip(shape_nums,shape_sizes):
        shape_frac_w = shape_size[0]/b_w
        shape_frac_h = shape_size[1]/b_h

        buffer_w = int(b_w * 0.02)
        buffer_h = int(b_h * 0.02)

        min_w = buffer_w
        max_w = b_w - buffer_w - shape_size[0]
        min_h = buffer_h
        max_h = b_h - buffer_h - shape_size[1]
        pos_x = random.randint(min_w, max_w)
        pos_y = random.randint(min_h, max_h)

        pos_x_frac = pos_x / b_w
        pos_y_frac = pos_y / b_h

        locations.append((pos_x,pos_y))
        bbox.append(f'{shape_num} {pos_x_frac} {pos_y_frac} {shape_frac_w} {shape_frac_h}\n')

    f = open(outfilename[:-4]+'.txt','w')
    f.writelines(bbox)
    f.close()
    if seamless:
        h.pasteImgsCV2(os.path.join(bkgd_dir,bkgd_fp),[os.path.join(shape_dir,s) for s in shape_fps],locations,outfilename)
    else:
        h.pasteImgsPIL(os.path.join(bkgd_dir, bkgd_fp), [os.path.join(shape_dir, s) for s in shape_fps], locations,outfilename)

