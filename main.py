from PyInquirer import prompt
from PyInquirer.separator import Separator
from numpy.lib.npyio import save
from simpleImage import SimpleImage

questions = [
    {
        'type': 'list',
        'name': 'InterpolationAlgo',
        'message': 'Por qual método você deseja realizar a interpolação?',
        'choices': [
            'Interpolação por vizinho mais próximo',
            'Interpolação bilinear',
            Separator(),
            'Transformar para grayscale!'
        ]
    },
    {
        'type': 'list',
        'name': 'InterpolationType',
        'message': 'Escolha o tipo de interpolação: ',
        'choices': [
            'Ampliação',
            'Redução'
        ],
        'when': lambda ans: ans['InterpolationAlgo'] != 'Transformar para grayscale!'
    },
    {
        'type': 'confirm',
        'name': 'save',
        'message': "Você deseja salvar a imagem resultante ?"
    }
]


if __name__ == "__main__":
    results = prompt(questions)

    image = SimpleImage('amogus.png', save_file=results['save'])

    if 'Transformar para grayscale!' in results.values():
        print(image.data.shape)
        image.in_grayscale()
    else:
        image.interpolacao_vizinhos_ampliacao()