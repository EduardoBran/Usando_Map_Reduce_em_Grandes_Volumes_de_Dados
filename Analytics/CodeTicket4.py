from mrjob.job import MRJob
from mrjob.step import MRStep

class InfracoesPorMarcaVeiculo(MRJob):


    def steps(self):
        return [
            MRStep(mapper=self.mapper_get_marca_veiculo_infracao,
                   reducer=self.reducer_count_infracoes),
            MRStep(reducer=self.reducer_top_veiculos)
        ]

    # Mapper: Extrai a marca de veículo de cada linha
    def mapper_get_marca_veiculo_infracao(self, _, line):

    	fields = line.split(',')

    	if fields[0].isdigit():
    		try:
    			# Extrair a marca de veículo (Vehicle Make)
    			marca = fields[7].strip().upper() if fields[7].strip() else "unknown"

    			# Emitir a marca do veículo
    			yield marca, 1

    		except IndexError:
    			return

    # Reducer: Soma as ocorrências de cada marca de veículo
    def reducer_count_infracoes(self, key, values):
    	yield None, (sum(values), key)


    # Reducer final: Seleciona os tipos de veículos com mais infrações
    def reducer_top_veiculos(self, _, marca_veiculo_contagem):

    	# Ordena pela contagem e exibe todos as marcas de veiculos
    	sorted_veiculos = sorted(marca_veiculo_contagem, reverse=True, key=lambda x: x[0])

    	for count, marca in sorted_veiculos:
    		yield marca, count



if __name__ == '__main__':
    InfracoesPorMarcaVeiculo.run()