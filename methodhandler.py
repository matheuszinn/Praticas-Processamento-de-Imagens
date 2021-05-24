from simpleImage import SimpleImage


class MethodHandler:

    def __init__(self, image: SimpleImage) -> None:

        self.metodos = {
            "Interpolação": image.interpolação,
            "Reflexão/Espelhamento": image.reflexão_espelhamento,
            "Transformar em negativo": image.negativo,
            "Operação aritmética": image.aritmetica,
            "Equalizar histograma normalizado": image.histograma
        }

    def execute(self, options: dict) -> None:
        if 'opt' in options:
            self.metodos[options['operation']](options['opt'])
        else:
            self.metodos[options['operation']]()
