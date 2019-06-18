import matplotlib.pyplot as plt
import skimage as ski

pic = ski.io.imread('grid.png', as_gray=True)

fig, axes = plt.subplots(1, 1)

pic[250][250] = 0

print(pic[250][251])

pic[250][250] = pic[260][260]

axes.imshow(pic, cmap=plt.cm.gray)

plt.show()
