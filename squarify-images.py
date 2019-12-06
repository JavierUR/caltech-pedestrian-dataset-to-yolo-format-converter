import glob
from PIL import Image
import threading
import tqdm

frame_size = (640, 640)
new_size = (416,416)
directory = 'images'
out_dir = 'squared'

if not os.path.exists(out_dir):
	os.makedirs(out_dir)

num_threads = 16
threads = []

def squarify(frame):
	new_frame = Image.new('RGB', frame_size, 'white')
	new_frame.paste(Image.open(frame), (0, 0))
	new_frame.thumbnail(new_size,PIL.Image.ANTIALIAS)

	new_frame_path = frame.replace('.png', '_squared.png')
	new_frame_path = new_frame_path.replace(directory, out_dir)
	new_frame.save(new_frame_path, 'png')

	#print('saved ' + new_frame_path)

for frame in tqdm(sorted(glob.glob(directory + '/*.png'))):
	# enlarge 640 x 480 frames up to frame_size 
	# by filling the bottom area with whitespace
	threads.append(threading.Thread(target = squarify, args=(frame,)))
	if len(threads) == num_threads:
		[ t.start() for t in threads ]
    	[ t.join() for t in threads ]
	