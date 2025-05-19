import os
import sys

from PIL import Image

def create_gif(folder:str, output_gif_filename:str):
    frames = []
    durations = []
    image_files = []
    for image_file in os.listdir(folder):
        if image_file.endswith(".png"):
            image_files.append(image_file)
    image_files.sort(key=lambda x: int(x.strip('plot-').split(".")[0]))
    for image_file in image_files:
        image = Image.open(os.path.join(folder, image_file))
        frames.append(image)
        durations.append(500)
    durations[-1] = 3000
    frames[0].save(
        output_gif_filename,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0
    )



if __name__ == '__main__':
    if sys.argv.__len__() < 3:
        print("Usage: python create_gif.py folder output_gif_filename")
        print('Example: python create_gif.py ../assets/image/solution/ts ../assets/image/ts.gif')
        sys.exit(1)
    create_gif(sys.argv[1], sys.argv[2])