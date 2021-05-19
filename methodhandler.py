from simpleImage import SimpleImage


class MethodHandler:

    def __init__(self, image: SimpleImage) -> None:

        self.metodos = {
            "Interpolação": image.interpolação,
            "Transformar em cinza": image.in_grayscale,
            "Reflexão/Espelhamento": image.reflexão_espelhamento,
            "Transformar em negativo": image.negativo
        }

    def execute(self, options: dict) -> None:
        if 'opt' in options:
            self.metodos[options['operation']](options['opt'])
        else:
            self.metodos[options['operation']]()
