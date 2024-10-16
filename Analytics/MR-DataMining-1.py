from mrjob.job import MRJob


class MRDataMining(MRJob):

    def mapper(self, _, line):
        palavras = line.split()
        for palavra in palavras:
            yield palavra.lower(), 1

    def reducer(self, key, values):
        yield key, sum(values)


if __name__ == '__main__':
    MRDataMining.run()


