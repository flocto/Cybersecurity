from PIL import Image

img = Image.open('elf.png')
bounds = (215, 215, 335, 333)

crop = img.crop(bounds)
# crop.save('extract.png')

# 2 by 2 blocks
block_size = 2

dat = []
# start from top right, go left to right, top to bottom
for y in range(0, crop.height, block_size):
    for x in range(crop.width - block_size, -1, -block_size):
        block = crop.crop((x, y, x + block_size, y + block_size))
        byt = block.getpixel((0, 0))
        r, g, b, _ = byt
        dat.extend([r, g, b])

open('dump.bin', 'wb').write(bytes(dat))