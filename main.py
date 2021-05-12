from methodhandler import MethodHandler
from PyInquirer import prompt
from PyInquirer.separator import Separator
from simpleImage import SimpleImage

questions = [
    {
        'type': 'list',
        'name': 'operation',
        'message': 'O que deseja fazer com a imagem ?',
        'choices': [
            'Interpolação',
            Separator(),
            'Transformar em cinza'
        ]
    },
    {
        'type': 'list',
        'name': 'interpolationAlgo',
        'message': 'Por qual método você deseja realizar a interpolação?',
        'choices': [
            'Vizinho mais próximo',
            'Bilinear',
        ],
        'when' : lambda x : x['operation'] == 'Interpolação'
    },
    {
        'type': 'list',
        'name': 'interpolationType',
        'message': 'Escolha o tipo de interpolação: ',
        'choices': [
            'Ampliação',
            'Redução'
        ],
        'when': lambda ans: 'Interpolação' in ans.values()
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

if __name__ == "__main__":
    results = prompt(questions)

    image = SimpleImage(results['imgPath'], save_f=results['save'])
    print(image.mode)
    handler = MethodHandler(image)

    if 'Transformar em cinza' in results.values():
        handler.metodos[results['operation']]()
    else: 
        handler.execute(
            results['operation'],
            results['interpolationAlgo'],
            results['interpolationType']
            )