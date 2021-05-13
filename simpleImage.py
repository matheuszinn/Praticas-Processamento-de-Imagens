from PIL import Image
import numpy as np

class SimpleImage:

    def __init__(self, imgPath: str, save_f:bool=False) -> None:
        self.imgPath = imgPath
        self.image = Image.open(self.imgPath)
        self.pixel_data = self.image.load()
        self.data = np.asarray(self.image)
        self.width = self.image.width
        self.heigth = self.image.height
        self.save_f = save_f
        self.mode = self.image.mode

    def save_file(self,name: str ,image) -> None:
        if self.save_f:
            image.save(f'{name}_{self.imgPath}');

    def in_grayscale(self) -> None:

        def set_grayscale(values: tuple) -> list:
            mean = sum(values) // 3 
            return [mean, mean, mean] if self.mode == "RGB" else [mean, mean, mean, values[3]] 

        temp = []
        for rows in self.data:
            pixel_list = []
            for pixel in rows:
                pixel_list.append(set_grayscale(pixel))
            temp.append(pixel_list)
        
        data = np.array(temp, dtype=np.uint8)
        newImage = Image.fromarray(data)
        newImage.show()
        self.save_file(f"Gray", newImage)

    def interpolacao_vizinhos_reducao(self) -> None:
        imgList = []
        for y in range(0, self.heigth-1,2):
            row = []
            for x in range(0, self.width-1,2):
                row.append(self.pixel_data[x,y])
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
                row.append(self.pixel_data[x,y])
                row.append(self.pixel_data[x,y])
            imgList.append(row)
            imgList.append(row)

        data = np.array(imgList, dtype=np.uint8)
        newImage = Image.fromarray(data)
        newImage.show()
        self.save_file('VizinhosAmpliação', newImage)

    def calcular_rgb_media(self, *val: tuple) -> list:
        
        r,g,b,a = 0,0,0,0
        for pixel in val:
            r += pixel[0]
            g += pixel[1]
            b += pixel[2]
            
        if self.mode == "RGBA":
            a = sum([ x[3] for x in val])
            return [i//len(val) for i in [r,g,b,a]]   
             
        return [i//len(val) for i in [r,g,b]]      

    def interpolacao_bilinear_reducao(self) -> None:

        imgList = []
        for y in range(0, self.heigth - 1,2):
            row = []
            for x in range(0, self.width - 1, 2):
                row.append(self.calcular_rgb_media(
                    self.pixel_data[x,y],
                    self.pixel_data[x,y+1],
                    self.pixel_data[x+1,y],
                    self.pixel_data[x+1,y+1]
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
            middleRow=[]
            for x in range(self.width):
                if x == self.width-1 or y == self.heigth-1:
                    row.append(self.pixel_data[x, y])
                    row.append(self.pixel_data[x, y])
                    
                    middleRow.append(self.pixel_data[x,y])
                    middleRow.append(self.pixel_data[x,y])

                else:
                    row.append(self.pixel_data[x, y])
                    row.append(self.calcular_rgb_media( 
                        self.pixel_data[x, y],
                        self.pixel_data[x, y+1]
                    ))

                    middleRow.append(self.calcular_rgb_media(
                        self.pixel_data[x,y],
                        self.pixel_data[x+1, y]
                    ))

                    middleRow.append(self.calcular_rgb_media(
                        self.pixel_data[x, y],
                        self.pixel_data[x, y+1],
                        self.pixel_data[x+1,y+1],
                        self.pixel_data[x+1, y]
                    ))

            imgList.append(row)
            imgList.append(middleRow)

        data = np.array(imgList, dtype=np.uint8)
        newImage = Image.fromarray(data)
        newImage.show()
        self.save_file('BilinearAmpliação', newImage)
