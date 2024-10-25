from mrjob.job import MRJob
import re                    # Importa a biblioteca regex para trabalhar com expressões regulares
from heapq import nlargest    # Importa nlargest para selecionar os 20 maiores valores

class MRAvaliaFilme(MRJob):
    
    def mapper(self, key, line):
        # Regex para extrair as partes do log
        # Cada parte do padrão regex é configurada para capturar as diferentes informações da linha de log
        log_pattern = re.compile(
            r'^(?P<ip>\S+) '           # Captura o endereço IP: \S+ significa "qualquer sequência de caracteres que não seja espaço"
            r'(?P<identd>\S+) '        # Captura o Identd do cliente: também é uma sequência sem espaços (geralmente '-')
            r'(?P<user>\S+) '          # Captura o nome do usuário autenticado (geralmente '-' se não autenticado)
            r'\[(?P<timestamp>.*?)\] ' # Captura o timestamp (data e hora): .*? captura qualquer coisa entre colchetes
            r'"(?P<request>.*?)" '     # Captura a requisição HTTP: qualquer coisa entre aspas (por exemplo, "GET /index.html HTTP/1.1")
            r'(?P<status>\d{3}) '      # Captura o código de status HTTP: \d{3} significa "exatamente três dígitos" (ex: 200, 404)
            r'(?P<size>\S+)'           # Captura o tamanho do objeto retornado: \S+ captura qualquer sequência que não seja espaço (ex: 5120 bytes ou '-')
        )

        # Aplicar regex à linha
        match = log_pattern.match(line)  # 'match' tenta aplicar o padrão à linha do log e retorna um objeto match se for bem-sucedido
        
        if match:
            # Extrair o IP do objeto match
            ip = match.group('ip')  # 'group' retorna a parte capturada pelo nome do grupo (neste caso, 'ip' é o endereço IP)
            
            # Emitir o IP com valor 1, indicando uma conexão
            yield ip, 1  # O Mapper emite o endereço IP e o valor 1, que será somado no reducer

    def reducer(self, ip, occurrences):
        # Armazenar as contagens de IPs em uma lista
        self.ip_counts = getattr(self, 'ip_counts', [])
        self.ip_counts.append((ip, sum(occurrences)))

    def reducer_final(self):
        # Selecionar os 20 IPs com mais conexões
        top_20_ips = nlargest(20, self.ip_counts, key=lambda x: x[1])
        
        # Emitir os 20 maiores IPs
        for ip, total in top_20_ips:
            yield ip, total

if __name__ == '__main__':
    MRAvaliaFilme.run()  # Executa o job de MapReduce

