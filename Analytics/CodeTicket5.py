from mrjob.job import MRJob
from mrjob.step import MRStep

class InfracoesPorNomeRua(MRJob):


    def steps(self):
        return [
            MRStep(mapper=self.mapper_get_nome_rua_infracao,
                   reducer=self.reducer_count_infracoes),
            MRStep(reducer=self.reducer_top_nomes_ruas)
        ]

    # Mapper: Extrai o nome de rua de cada linha
    def mapper_get_nome_rua_infracao(self, _, line):

    	fields = line.split(',')

    	if fields[0].isdigit():
    		try:
    			# Extrair o nome da rua (Street Name)
    			nome_rua = fields[24].strip().upper() if fields[24].strip() else "unknown"

    			# Emitir a marca do veículo
    			yield nome_rua, 1

    		except IndexError:
    			return

    # Reducer: Soma as ocorrências de cada nome de rua
    def reducer_count_infracoes(self, key, values):
    	yield None, (sum(values), key)


    # Reducer final: Seleciona os nomes de ruas com mais infrações
    def reducer_top_nomes_ruas(self, _, nome_ruas):

        # Ordena pela contagem em ordem decrescente e exibe todos os nomes de ruas
        ruas_ordenadas = sorted(nome_ruas, reverse=True, key=lambda x: x[0])
        
        for count, nome in ruas_ordenadas:
            # Exibe apenas ruas com 10000 ou mais infrações
            if count >= 1000:
                yield nome, count


if __name__ == '__main__':
    InfracoesPorNomeRua.run()