from simpleImage import SimpleImage


class MethodHandler:

    def __init__(self, image: SimpleImage) -> None:

        self.metodos = {
            "Interpolação": image.interpolação,
            "Operação aritmética": image.aritmetica,
            "Operação geométrica": image.reflexão_espelhamento,
            "Transformação de intensidade": image.intensidade
        }

    def execute(self, options: dict) -> None:
        if 'opt' in options:
            self.metodos[options['operation']](options['opt'])
        else:
            self.metodos[options['operation']]()
