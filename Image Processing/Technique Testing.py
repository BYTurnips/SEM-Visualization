from scipy import ndimage as ndi
import skimage as ski
import skimage.morphology as morph
from skimage.color import label2rgb
from skimage.feature import canny
import matplotlib.pyplot as plt

img = ski.io.imread('Cap403border.png', as_gray=True)
edges = canny(img, sigma=3.5)
edges = morph.dilation(edges)
filled = ndi.binary_fill_holes(edges)
filled = morph.erosion(filled)
filled = morph.remove_small_objects(filled, min_size=70)
labeled, _ = ndi.label(filled)

image_label_overlay = label2rgb(labeled, image=filled)

fig, axes = plt.subplots(1, 2, figsize=(8, 3), sharey=True)
axes[0].imshow(img, cmap=plt.cm.gray, interpolation='nearest')
axes[0].contour(filled, [0.5], linewidths=1.2, colors='y')
axes[1].imshow(image_label_overlay, interpolation='nearest')

_, ax = plt.subplots(figsize=(4, 3))
ax.imshow(filled, cmap=plt.cm.gray, interpolation='nearest')
ax.set_title('filling the holes')
ax.axis('off')
plt.show()
