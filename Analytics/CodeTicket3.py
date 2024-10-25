from mrjob.job import MRJob
from mrjob.step import MRStep

class InfracoesPorTipoVeiculo(MRJob):

    def steps(self):
        return [
            MRStep(mapper=self.mapper_get_veiculo_infracao,
                   reducer=self.reducer_count_infracoes),
            MRStep(reducer=self.reducer_top_veiculos)
        ]

    # Mapper: Extrai o tipo de veículo de cada linha
    def mapper_get_veiculo_infracao(self, _, line):
        fields = line.split(',')
        
        if fields[0].isdigit():
            try:
                # Extrair o tipo de veículo (Vehicle Body Type)
                tipo_veiculo = fields[6].strip().upper() if fields[6].strip() else "unknown"  # Posição 6 para Vehicle Body Type
                
                # Emitir o tipo de veículo (substitui por 'unknown' se estiver ausente/nulo)
                yield tipo_veiculo, 1
                
            except IndexError:
                return

    # Reducer: Soma as ocorrências de cada tipo de veículo
    def reducer_count_infracoes(self, key, values):
        yield None, (sum(values), key)

    # Reducer final: Seleciona os tipos de veículos com mais infrações
    def reducer_top_veiculos(self, _, tipo_veiculo_contagem):
        # Ordena pela contagem e exibe todos os tipos de veículos relevantes
        sorted_veiculos = sorted(tipo_veiculo_contagem, reverse=True, key=lambda x: x[0])
        for count, tipo_veiculo in sorted_veiculos:
            yield tipo_veiculo, count

if __name__ == '__main__':
    InfracoesPorTipoVeiculo.run()

