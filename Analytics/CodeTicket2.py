from mrjob.job import MRJob
from mrjob.step import MRStep

class InfracoesPorTempo(MRJob):

    def steps(self):
        return [
            MRStep(mapper=self.mapper_get_tempo_infracao,
                   reducer=self.reducer_count_tempo),
            MRStep(reducer=self.reducer_top_20_tempos)
        ]

    # Mapper: Extrai o tempo da infração de cada linha
    def mapper_get_tempo_infracao(self, _, line):
        fields = line.split(',')
        
        if fields[0].isdigit():
            try:
                # Extrair o tempo (Violation Time)
                tempo = fields[19].strip()  # Posição 19 para Violation Time
                
                if not tempo:
                    tempo = 'unknown'
                
                yield tempo, 1
                
            except IndexError:
                return

    # Reducer: Soma as ocorrências de cada tempo
    def reducer_count_tempo(self, key, values):
        yield None, (sum(values), key)

    # Reducer final: Seleciona os 20 tempos com mais ocorrências
    def reducer_top_20_tempos(self, _, tempo_contagem):
        # Ordena pela contagem (primeiro valor na tupla) e seleciona os 20 maiores
        sorted_tempos = sorted(tempo_contagem, reverse=True, key=lambda x: x[0])
        for count, tempo in sorted_tempos[:20]:
            yield tempo, count

if __name__ == '__main__':
    InfracoesPorTempo.run()

