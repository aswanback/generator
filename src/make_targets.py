import argparse
import os
import generation as g

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='dataset generation')
    parser.add_argument('dst_dir',metavar='-d',help='destination directory')
    parser.add_argument('number_each',metavar='-n',help='number of targets of each type to make')
    parser.add_argument('size',help='size of target image square')
    parser.add_argument('--font_size',default=0,help='font size')
    parser.add_argument('--clean',help='wipe the target directory before running',action='store_true')
    args = parser.parse_args()
    if args.dst_dir not in os.listdir():
        os.system(f'mkdir {args.dst_dir}')
    if args.font_size == 0: args.font_size = int(args.size)/2

    g.generateTargetDataset(args.dst_dir,int(args.number_each),int(args.size),int(args.font_size),clear_dir=args.clean,bkgd_format='png')

    ## If you would like to call this from within an IDE, use the below
    # g.generateTargetDataset(target_dir=dst_dir, num_each=n, shape_size=s, font_size=f,clear_dir=False, bkgd_format='png')
