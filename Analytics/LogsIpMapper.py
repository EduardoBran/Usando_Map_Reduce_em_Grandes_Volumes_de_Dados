#!/usr/bin/env python

#!/usr/bin/env python

import sys
import re

# Regex para extrair o endereço IP
log_pattern = re.compile(
    r'^(?P<ip>\S+) '           # Captura o endereço IP
    r'(?P<identd>\S+) '        # Ignora o Identd
    r'(?P<user>\S+) '          # Ignora o usuário
    r'\[(?P<timestamp>.*?)\] ' # Ignora o timestamp
    r'"(?P<request>.*?)" '     # Ignora a requisição
    r'(?P<status>\d{3}) '      # Ignora o status
    r'(?P<size>\S+)'           # Ignora o tamanho
)

for line in sys.stdin:
    # Aplicar regex à linha
    match = log_pattern.match(line)
    if match:
        ip = match.group('ip')
        print(ip)
