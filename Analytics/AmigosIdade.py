from mrjob.job import MRJob

class MRAmigosPorIdade(MRJob):

    def mapper(self, _, line):
        (ID, nome, idade, numAmigos) = line.split(',')
        yield idade, float(numAmigos)

    def reducer(self, idade, numAmigos):
        total = 0
        numElementos = 0
        for x in numAmigos:
            total += x
            numElementos += 1
            
        yield idade, total / numElementos


if __name__ == '__main__':
    MRAmigosPorIdade.run()

    