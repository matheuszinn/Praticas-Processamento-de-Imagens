from os import terminal_size
from PIL import Image
import numpy as np
from numpy.lib.npyio import save 

def get_blank() -> list:
    return [(0,0,0,255) for _ in range(1024)]

def set_grayscale(values:tuple) -> list:
    mean = (sum(values) - values[3]) // 3
    return [mean, mean, mean, values[3]]


class SimpleImage:

    def __init__(self, imgPath: str, save_file:bool=False) -> None:
        self.imgPath = imgPath
        self.image = Image.open(self.imgPath)
        self.pixel_data = self.image.load()
        self.data = np.asarray(self.image)
        self.width = self.image.width
        self.heigth = self.image.height
        self.size = self.image.size
        self.save_file = save_file

    def in_grayscale(self) -> None:
        temp = []
        for rows in self.data:
            column_list = []
            for column in rows:
                column_list.append(set_grayscale(column))
            temp.append(column_list)
        
        data = np.array(temp, dtype=np.uint8)
        newImage = Image.fromarray(data)
        newImage.show()


    def interpolacao_vizinhos_diminuicao(self) -> None:
        imgList = []
        for y in range(0, self.width-1,2):
            row = []
            for x in range(0, self.heigth-1,2):
                row.append(self.pixel_data[x,y])
            imgList.append(row)
        data = np.array(imgList, dtype=np.uint8)
        newImage = Image.fromarray(data)
        newImage.show()
        if self.save_file:
            newImage.save(f'Diminuição_{self.imgPath}')

    def interpolacao_vizinhos_ampliacao(self) -> None:
        imgList = []
        for y in range(self.width):
            row = []
            for x in range(self.width):
                row.append(self.pixel_data[x,y])
                row.append(self.pixel_data[x,y])
            imgList.append(row)
            imgList.append(get_blank())

        data = np.array(imgList, dtype=np.uint8)
        newImage = Image.fromarray(data)
        newImage.show()

        if self.save_file:
            newImage.save(f'Ampliação_{self.imgPath}')
            
