import pandas as pd
import numpy as np
from os import path
from PIL import Image
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def read_from_xlx(pathname, lbl_2d=False):
    if lbl_2d:
        df = pd.read_excel (pathname, header=1)
    else:
        df = pd.read_excel (pathname)
    return df

def split_string_based_on_char(my_string,separator='['):
    splited_string = my_string.split(sep=separator)
    return splited_string

def plot_results(words, title):
    mask = np.array(Image.open(path.join("./mouse.png")))

    listToStr = ' '.join([elem for elem in words]) 

    # Create and generate a word cloud image:
    wordcloud = WordCloud(width=1600, height=800,
                        background_color="white", max_words=2000, mask=mask,
                        max_font_size=4, min_font_size=4, colormap="Blues",
                        contour_width=2, contour_color='steelblue').generate(listToStr)

    # Display the generated image:
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.title(title)
    plt.show()    