from mrjob.job import MRJob
from mrjob.step import MRStep

class InfracoesPorBairro(MRJob):

    def steps(self):
        return [
            MRStep(mapper=self.mapper_get_bairro_infracao,
                   reducer=self.reducer_count_infracoes),
            MRStep(reducer=self.reducer_find_max_infracoes)
        ]

    # Mapper: Extrai o bairro e o código da infração de cada linha
    def mapper_get_bairro_infracao(self, _, line):
        # Usando vírgula como delimitador (formato CSV)
        fields = line.split(',')
        
        # Ignorando o cabeçalho (garantindo que os campos são numéricos)
        if fields[0].isdigit():  
            try:
                # Extrair o bairro (Violation Location) e o código da infração (Violation Code)
                bairro = fields[14].strip()  # Posição 14 para Violation Location
                codigo_infracao = fields[5].strip()  # Posição 5 para Violation Code
                
                # Verificando se o bairro está vazio
                if not bairro:
                    return
                
                # Se o código de infração estiver ausente, defina como 'unknown'
                if not codigo_infracao:
                    codigo_infracao = 'unknown'
                
                # Emitir o bairro e o código da infração como chave, e o valor 1 para contar
                yield (bairro, codigo_infracao), 1
                
            except IndexError:
                # Caso ocorra erro de índice, a linha pode estar malformada e será ignorada
                return

    # Reducer: Soma as ocorrências de cada (bairro, tipo de infração)
    def reducer_count_infracoes(self, key, values):
        yield key[0], (sum(values), key[1])

    # Reducer final: Determina a infração mais comum por bairro
    def reducer_find_max_infracoes(self, bairro, infracoes_contadas):
        yield bairro, max(infracoes_contadas)  # max() retorna a infração mais frequente

if __name__ == '__main__':
    InfracoesPorBairro.run()

