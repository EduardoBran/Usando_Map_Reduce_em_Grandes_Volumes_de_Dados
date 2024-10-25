#!/usr/bin/env python

import sys

current_ip_address = None
current_ip_address_count = 0

# Itera sobre cada linha recebida do Mapper
for line in sys.stdin:
    line = line.strip()
    
    # Verifica se a linha está vazia (ignora linhas vazias)
    if not line:
        continue
    
    # O Mapper emite apenas o IP, por isso espera-se uma única coluna
    try:
        new_ip_address = line
    except ValueError:
        # Se houver algum erro inesperado, continue
        continue

    # Se o IP atual mudar, imprime o IP anterior e sua contagem
    if current_ip_address and current_ip_address != new_ip_address:
        print("{0}\t{1}".format(current_ip_address, current_ip_address_count))
        current_ip_address_count = 0

    # Atualiza o IP atual e incrementa sua contagem
    current_ip_address = new_ip_address
    current_ip_address_count += 1

# Após iterar, imprime o último IP e sua contagem
if current_ip_address:
    print("{0}\t{1}".format(current_ip_address, current_ip_address_count))
