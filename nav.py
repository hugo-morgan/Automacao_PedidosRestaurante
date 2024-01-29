pedido = """AAAA
BBBB
CCCC
DDDD"""

pedido = pedido.split()
pedido_text = ''

for _ in pedido:
    pedido_text = pedido_text + _ + '%0A'


print(pedido_text)