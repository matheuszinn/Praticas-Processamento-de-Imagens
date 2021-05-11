const {SimpleImageClass} = require('./SimpleImageClass.js');
const inquirer = require('inquirer');

const image = new SimpleImageClass('amogus.png');

inquirer.prompt([
    {
        type: 'list',
        name: 'InterpolationAlgo',
        message: 'Por qual método você deseja realizar a interpolação?',
        choices: [
            'Interpolação por vizinho mais próximo',
            'Interpolação bilinear',
            new inquirer.Separator(),
            'Transformar em cinza!'
        ]
    },
    {
        type: 'list',
        name: 'InterpolationType',
        message: 'Escolha o tipo de interpolação:',
        choices: [
            'Redução',
            'Ampliação'
        ],
        when: (answers) => {
            return answers.InterpolationAlgo !== 'Transformar em cinza!'
        }
    }
]).then( (answers) => {
    if(Object.keys(answers).length === 1){
        console.log(`Transformando o arquivo ${image.imgPath} em cinza!`);
        image.metodos[answers.InterpolationAlgo]();
    }else{
        console.log(answers);
        image.metodos[answers.InterpolationAlgo](answers.InterpolationType);
    }
});