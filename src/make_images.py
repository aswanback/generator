import argparse
import os
import generation as g

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='dataset generation')
    parser.add_argument('dst_dir',metavar='-d',help='destination directory')
    parser.add_argument('shape_dir', metavar='-s',help='source of shape images')
    parser.add_argument('bkgd_dir', metavar='-b',help='source of background images')
    parser.add_argument('number',metavar='-n',help='number of images to make')
    parser.add_argument('--targets',default=1,help='number of shapes in each background')
    parser.add_argument('--seamless',help='Use cv2 seamless method',action='store_true')
    parser.add_argument('--clean',help='wipe the target directory before running',action='store_true')
    args = parser.parse_args()
    if args.dst_dir not in os.listdir():
        os.system(f'mkdir {args.dst_dir}')
    if args.clean:
        os.system(f'rm {args.dst_dir}/*')

    for j in range(int(args.number)):
        i = 0
        fname = f'im-{args.targets}-{i}.png'
        while fname in os.listdir(args.dst_dir):
            i += 1
            fname = f'im-{args.targets}-{i}.png'
        g.generateImgAndTxt(f'{args.dst_dir}/{fname}', args.shape_dir, args.bkgd_dir, int(args.targets),args.seamless)

    ## If you would like to call this function from within an IDE, use the below
    # g.generateImgAndTxt(outfilename=f'{dst_dir}/{filename}', shape_dir=s, bkgd_dir=b, num_targets=1,seamless=False)