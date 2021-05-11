const {Image} = require('image-js');
const imgPath = 'amogus.png';

class SimpleImageClass{

    constructor(imgPath){
        this.imgPath = imgPath;
        this.metodos = {
            "Interpolação por vizinho mais próximo": (opt) =>{
                if(opt === "Ampliação"){
                    this.interpolaçãoVizinhosProximosAumento()
                }else{
                    this.interpolaçãoVizinhosProximosReducao()
                }
            },
            "Interpolação bilinear" : (opt) => {
                if(opt === "Ampliação"){
                    this.interpolaçãoBilinearAumento();
                }else{
                    this.interpolaçãoBilinearReducao();
                }
            },
            "Transformar em cinza!" : () => {
                this.inGrayscale();
            }
        };
    }

    #setPixelGreyscale(pixel){
        let mean = (pixel.reduce((a,b) => a+b) - pixel[3]) / 3;
        return [mean, mean, mean, pixel[3]];
    }

    inGrayscale(){
        Image.load(this.imgPath).then( (image) => {
            let pixels = [];
            for(let x = 0; x < image.width; x++){
                for(let y = 0; y < image.height; y++){
                    pixels.push(this.#setPixelGreyscale(image.getPixelXY(y,x)));
                }
            }
            const n = new Image(image.width, image.height, pixels.flat());
            n.save('Pgrey_' + this.imgPath);
        });
    }

    interpolaçãoBilinearAumento(){
        console.log("Aumento com interpolação bilinear")
    }

    interpolaçãoBilinearReducao(){
        console.log("Redução com interpolação bilinear")
    }

    interpolaçãoVizinhosProximosAumento(){
        Image.load(this.imgPath).then((image) => {
            let pixels = [];
            for(let y = 0; y < image.height;y++){
                for(let x = 0; x < image.width; x++){
                    //TODO: Falta terminar isso aqui!!
                    console.log(`Pixel(${x},${y}): [${image.getPixelXY(x,y)}]`);       
                }
            } 
        });
    }

    interpolaçãoVizinhosProximosReducao(){
        Image.load(this.imgPath).then((image) => {
            let pixels = [];
            for(let y = 0; y < image.height;y+=2){
                for(let x = 0; x < image.width; x+=2){
                    pixels.push(image.getPixelXY(x,y));
                }
            }
            const newImage = new Image(image.width / 2 , image.height / 2, pixels.flat());
            newImage.save(`VizinhoRedução(${newImage.width}x${newImage.height})_${this.imgPath}`);
        });
    }

}

module.exports = {SimpleImageClass};