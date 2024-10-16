from mrjob.job import MRJob
import re

REGEXP_PALAVRA = re.compile(r"[\w']+")

class MRDataMining(MRJob):

    def mapper(self, _, line):
        palavras = REGEXP_PALAVRA.findall(line)
        for palavra in palavras:
            yield palavra.lower(), 1

    def reducer(self, key, values):
        yield key, sum(values)


if __name__ == '__main__':
    MRDataMining.run()

