from simpleImage import SimpleImage

# Classe para registrar os métodos novos, e fazer o prompt funcionar

class MethodHandler:

    def __init__(self, image: SimpleImage) -> None:
        
        self.metodos = {
            "Interpolação": {
                "Vizinho mais próximo": {
                    "Ampliação": image.interpolacao_vizinhos_ampliacao,
                    "Redução": image.interpolacao_vizinhos_reducao
                },
                "Bilinear": {
                    "Ampliação": image.interpolacao_bilinear_ampliacao,
                    "Redução": image.interpolacao_bilinear_reducao
                }
            },
            "Transformar em cinza": image.in_grayscale
        }

    def execute(self, *vals: str):
        self.metodos[vals[0]] \
                    [vals[1]] \
                    [vals[2]]()