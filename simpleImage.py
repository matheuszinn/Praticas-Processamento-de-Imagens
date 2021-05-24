from os import strerror
from typing import Union
import numpy as np
from PIL import Image
from PyInquirer import prompt
from utils import MAT_ESP, MAT_REF, MAT_TESTE, IMPORTER
import matplotlib.pyplot as plt
from decimal import Decimal

# TODO: Transformar isso aqui em várias classes 

IMG_FOLDER = ""
OUT_FOLDER = "./out/"


class SimpleImage:

    def __init__(self, imgName: str, save_f: bool = False) -> None:
        self.imgName = imgName
        self.imgPath = IMG_FOLDER + imgName
        self.image = Image.open(self.imgPath)
        self.pixel_data = self.image.load()
        self.data = np.asarray(self.image)
        self.width = self.image.width
        self.heigth = self.image.height
        self.save_f = save_f
        self.mode = self.image.mode

    def save_file(self, name: str, image) -> None:
        if self.save_f:
            image.save(f'{OUT_FOLDER}{name}_{self.imgName}')

    def in_grayscale(self):
        img = self.image.convert('L')
        self.save_file("Grayscale", img)
        return img

    def interpolação(self, type: str) -> None:
        if 'Vizinho' in type:
            if 'Ampliação' in type:
                self.interpolacao_vizinhos_ampliacao()
            else:
                self.interpolacao_vizinhos_reducao()
        elif 'Bilinear' in type:
            if 'Ampliação' in type:
                self.interpolacao_bilinear_ampliacao()
            else:
                self.interpolacao_bilinear_reducao()

    def interpolacao_vizinhos_reducao(self) -> None:
        imgList = []
        for y in range(0, self.heigth-1, 2):
            row = []
            for x in range(0, self.width-1, 2):
                row.append(self.pixel_data[x, y])
            imgList.append(row)
        data = np.array(imgList, dtype=np.uint8)
        newImage = Image.fromarray(data)
        newImage.show()
        self.save_file('VizinhosRedução', newImage)

    def interpolacao_vizinhos_ampliacao(self) -> None:
        imgList = []
        for y in range(self.heigth):
            row = []
            for x in range(self.width):
                row.append(self.pixel_data[x, y])
                row.append(self.pixel_data[x, y])
            imgList.append(row)
            imgList.append(row)

        data = np.array(imgList, dtype=np.uint8)
        newImage = Image.fromarray(data)
        newImage.show()
        self.save_file('VizinhosAmpliação', newImage)

    def calcular_rgb_media(self, *val: tuple) -> list:

        r, g, b, a = 0, 0, 0, 0
        for pixel in val:
            r += pixel[0]
            g += pixel[1]
            b += pixel[2]

        if self.mode == "RGBA":
            a = sum([x[3] for x in val])
            return [i//len(val) for i in [r, g, b, a]]

        return [i//len(val) for i in [r, g, b]]

    def interpolacao_bilinear_reducao(self) -> None:

        imgList = []
        for y in range(0, self.heigth - 1, 2):
            row = []
            for x in range(0, self.width - 1, 2):
                row.append(self.calcular_rgb_media(
                    self.pixel_data[x, y],
                    self.pixel_data[x, y+1],
                    self.pixel_data[x+1, y],
                    self.pixel_data[x+1, y+1]
                ))

            imgList.append(row)
        data = np.array(imgList, dtype=np.uint8)
        newImage = Image.fromarray(data)
        newImage.show()
        self.save_file('BilinearRedução', newImage)

    def interpolacao_bilinear_ampliacao(self) -> None:

        imgList = []
        for y in range(self.heigth):
            row = []
            middleRow = []
            for x in range(self.width):
                if x == self.width-1 or y == self.heigth-1:
                    row.append(self.pixel_data[x, y])
                    row.append(self.pixel_data[x, y])

                    middleRow.append(self.pixel_data[x, y])
                    middleRow.append(self.pixel_data[x, y])

                else:
                    row.append(self.pixel_data[x, y])
                    row.append(self.calcular_rgb_media(
                        self.pixel_data[x, y],
                        self.pixel_data[x, y+1]
                    ))

                    middleRow.append(self.calcular_rgb_media(
                        self.pixel_data[x, y],
                        self.pixel_data[x+1, y]
                    ))

                    middleRow.append(self.calcular_rgb_media(
                        self.pixel_data[x, y],
                        self.pixel_data[x, y+1],
                        self.pixel_data[x+1, y+1],
                        self.pixel_data[x+1, y]
                    ))

            imgList.append(row)
            imgList.append(middleRow)

        data = np.array(imgList, dtype=np.uint8)
        newImage = Image.fromarray(data)

        newImage.show()
        self.save_file('BilinearAmpliação', newImage)

    def reflexão_espelhamento(self, type: str) -> None:

        newImage = Image.new(self.mode, self.image.size)
        newImage_pixels = newImage.load()

        if type == "Espelhamento":
            for y in range(self.heigth):
                for x in range(self.width):
                    matrixCalc = np.dot(MAT_ESP, [x, y, 1])
                    newImage_pixels[x, y] = self.pixel_data[self.width -
                                                            1 + matrixCalc[0], matrixCalc[1]]
        elif type == "Reflexão":
            for y in range(self.heigth):
                for x in range(self.width):
                    matrixCalc = np.dot(MAT_REF, [x, y, 1])
                    newImage_pixels[x, y] = self.pixel_data[x,
                                                            self.heigth - 1 + matrixCalc[1]]
        else:
            for y in range(self.heigth):
                for x in range(self.width):
                    matrixCalc = np.dot(MAT_TESTE, [x, y, 1])
                    newImage_pixels[x, y] = self.pixel_data[self.width - 1 + matrixCalc[0],
                                                            self.heigth - 1 + matrixCalc[1]]

        newImage.show()
        self.save_file(type, newImage)

    def negativo(self) -> None:

        def inverterPixel(pixel: tuple):
            val = [255 - val for val in pixel]
            if self.mode == "RGB":
                return tuple(val)
            else:
                val[3] = pixel[3]
                return tuple(val)

        newImage = Image.new(self.mode, self.image.size)
        newImage_pixels = newImage.load()

        for y in range(self.heigth):
            for x in range(self.width):
                pixel = self.pixel_data[x, y]
                newImage_pixels[x, y] = inverterPixel(pixel)

        newImage.show()
        self.save_file("Negativo", newImage)

    def aritmetica(self, type: str) -> None:
        results = prompt(IMPORTER)
        img_2 = SimpleImage(results['imgPath'], False)
        self.adicao(img_2) if 'Adição' in type else self.subtracao(img_2)

    def adicao(self, second: 'SimpleImage') -> None:
        imgList = []
        for y in range(self.heigth):
            row = []
            for x in range(self.width):
                row.append(self.calcular_rgb_media(
                    self.pixel_data[x, y], second.pixel_data[x, y]))
            imgList.append(row)

        data = np.array(imgList, dtype=np.uint8)
        newImage = Image.fromarray(data)
        newImage.show()
        self.save_file('Adição', newImage)

    def subtracao(self, second: 'SimpleImage') -> None:

        def calcular_rgb(pixel1: tuple, pixel2: tuple) -> tuple:
            r = abs(pixel1[0] - pixel2[0])
            g = abs(pixel1[1] - pixel2[1])
            b = abs(pixel1[2] - pixel2[2])
            return (r, g, b)

        imgList = []
        for y in range(self.heigth):
            row = []
            for x in range(self.width):
                row.append(calcular_rgb(
                    self.pixel_data[x, y], second.pixel_data[x, y]))
            imgList.append(row)

        data = np.array(imgList, dtype=np.uint8)
        newImage = Image.fromarray(data)
        newImage.show()
        self.save_file('Subtração', newImage)

    def histograma(self) -> None:

        #No momento só funciona com imagens em grayscale, por isso a conversão parar grayscale
        #TODO: Fazer esse método ficar menos burro e funcionando pelo menos com RGB, morra canal alpha maldito

        g_img = self.in_grayscale()
        number_of_pixels = self.width * self.heigth

        newImage = Image.new(g_img.mode, g_img.size)
        newImage_pixels = newImage.load()

        hist = g_img.histogram()
        norm_hist = [Decimal.from_float(x / number_of_pixels) for x in hist]
    
        hist_equal = []
        count = 0
        for i in range(0, len(hist)):
            count = count + len(hist) * norm_hist[i]
            hist_equal.append(count)

        vals_table = [min(round(x), 255) for x in hist_equal]
        look_up_table = dict(zip([x for x in range(0, len(hist))], vals_table))

        for y in range(newImage.height):
            for x in range(newImage.width):
                newImage_pixels[x, y] = look_up_table[g_img.getpixel((x, y))]

        newImage_hist = newImage.histogram()

        fig, axes = plt.subplots(nrows=2, ncols=2)

        for i in range(len(hist)):
            axes[0, 0].set_title("Histograma da imagem")
            axes[0, 0].bar(i, hist[i], color="#000000", edgecolor="#000000")

        for i in range(len(hist)):
            axes[0, 1].set_title("Histograma normalizado")
            axes[0, 1].bar(i, norm_hist[i], color="#000000",
                           edgecolor="#000000")
            axes[0, 1].set_ylim(0, .1)

        hist_acum = []
        count = 0
        for i in range(0, len(norm_hist)):
            count += norm_hist[i]
            hist_acum.append(count)

        for i in range(len(hist)):
            axes[1, 0].set_title("Histograma normalizado c/ acúmulo")
            axes[1, 0].bar(i, norm_hist[i], color="#000000",
                           edgecolor="#000000")
            axes[1, 0].plot(hist_acum)

        for i in range(len(newImage_hist)):
            axes[1, 1].set_title('Histograma Equalizado')
            axes[1, 1].bar(i, newImage_hist[i],
                           color="#000000", edgecolor="#000000")

        plt.subplots_adjust(left=0.1,
                            bottom=0.1,
                            right=0.9,
                            top=0.9,
                            wspace=0.4,
                            hspace=0.4)

        plt.show()

        newImage.show()

        if self.save_f:
            fig.savefig(f"{OUT_FOLDER}Histogramas_{self.imgName}")
        self.save_file("Imagem_Equalizada", newImage)

    def intensidade(self, type: str) -> None:
        if type == 'Transformar em cinza':
            gray = self.in_grayscale()
            gray.show()
            self.save_file('Gray', gray)
        elif type == 'Transformar em negativo':
            self.negativo()
        else:
            self.histograma()
