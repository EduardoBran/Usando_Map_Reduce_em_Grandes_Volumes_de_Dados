from mrjob.job import MRJob
from mrjob.step import MRStep

class InfracoesPorCodigoRua(MRJob):

    def steps(self):
        return [
            MRStep(mapper=self.mapper_get_street_codes,
                   reducer=self.reducer_count_codes),
            MRStep(reducer=self.reducer_sort_top_codes)
        ]

    # Mapper: Extrai cada código de rua presente nas três colunas
    def mapper_get_street_codes(self, _, line):
        fields = line.split(',')
        
        if fields[0].isdigit():
            try:
                # Extrair os códigos de rua (Street Code1, Street Code2, Street Code3)
                street_codes = [fields[9].strip(), fields[10].strip(), fields[11].strip()]
                
                # Emitir cada código de rua válido como uma chave
                for code in street_codes:
                    if code:  # Ignorar códigos vazios
                        yield code, 1

            except IndexError:
                return  # Ignorar linhas com índice inválido

    # Reducer: Soma as ocorrências de cada código de rua
    def reducer_count_codes(self, code, counts):
        yield None, (sum(counts), code)

    # Reducer final: Ordena os códigos de rua por contagem de ocorrências
    def reducer_sort_top_codes(self, _, code_counts):
        # Ordena pela contagem em ordem decrescente
        sorted_codes = sorted(code_counts, reverse=True, key=lambda x: x[0])
        
        for count, code in sorted_codes:
            # Exibe apenas códigos com 10000 ou mais infrações
            if count >= 1000:
                yield code, count

if __name__ == '__main__':
    InfracoesPorCodigoRua.run()