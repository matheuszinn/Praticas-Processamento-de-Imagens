from methodhandler import MethodHandler
from PyInquirer import prompt
from simpleImage import SimpleImage
from utils import QUESTIONS

if __name__ == "__main__":
    results = prompt(QUESTIONS)
    image = SimpleImage(results['imgPath'], results['save'])
    handler = MethodHandler(image)
    handler.execute(results)