from PyInquirer.separator import Separator

# Constants that represent transformation matrices
MAT_ESP = ([-1, 0, 0], [0, 1, 0], [0, 0, 1])
MAT_REF = ([1, 0, 0], [0, -1, 0], [0, 0, 1])
MAT_TESTE = ([-1, 0, 0], [0, -1, 0], [0, 0, 1])


# Hold the questions asked by pyinquirer
QUESTIONS = [
    {
        'type': 'list',
        'name': 'operation',
        'message': 'O que deseja fazer com a imagem ?',
        'choices': [
            'Interpolação',
            'Operação aritmética',
            'Reflexão/Espelhamento',
            'Transformar em cinza',
            'Transformar em negativo'
        ]
    },
    {
        'type': 'list',
        'name': 'opt',
        'message': 'Escolha entre as opções.',
        'choices': [
            'Espelhamento',
            'Reflexão',
            'Espelhamento e Reflexão'
        ],
        'when': lambda x: x['operation'] == 'Reflexão/Espelhamento'
    },
    {
        'type': 'list',
        'name': 'opt',
        'message': 'Por qual método você deseja realizar a interpolação?',
        'choices': [
            'Ampliação por Vizinho mais próximo',
            'Redução Vizinho mais próximo',
            Separator(),
            'Ampliação por Bilinear',
            'Redução por Bilinear'
        ],
        'when': lambda x: x['operation'] == 'Interpolação'
    },
    {
        'type': 'list',
        'name': 'opt',
        'message': 'Qual operação aritmética deseja realizar?',
        'choices': [
            'Adição',
            'Subtração'
        ],
        'when': lambda x: x['operation'] == 'Operação aritmética'
    },
    
    {
        'type': 'input',
        'name': 'imgPath',
        'message': 'Entre com o nome do arquivo de imagem: '
    },
    {
        'type': 'confirm',
        'name': 'save',
        'message': "Você deseja salvar a imagem resultante ?"
    }
]

IMPORTER = [
    {
        'type': 'input',
        'name': 'imgPath',
        'message': 'Entre com o nome do arquivo de imagem: '
    }
]