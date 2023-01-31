import os
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--domain", "-d", default="sketch", help="Target")
parser.add_argument("--gpu", "-g", default=0, type=int, help="Gpu ID")
parser.add_argument("--times", "-t", default=1, type=int, help="Repeat times")

args = parser.parse_args()

###############################################################################
source = ["photo", "cartoon", "art_painting", "sketch"]
target = args.domain
source.remove(target)

input_dir = '/kaggle/working/CIRL/data/datalists'
output_dir = 'outputs'

config = "PACS/ResNet18"

domain_name = target
path = os.path.join(output_dir, config.replace("/", "_"), domain_name)
ckpt_path = os.path.join(path, 'best_model.tar')
##############################################################################

for i in range(args.times):
    os.system(f'CUDA_VISIBLE_DEVICES={args.gpu} '
              f'python test.py '
              f'--source {source[0]} {source[1]} {source[2]} '
              f'--target {target} '
              f'--input_dir {input_dir} '
              f'--output_dir {output_dir} '
              f'--config {config} '
              f'--ckpt {ckpt_path}')
