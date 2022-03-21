rxBuffer = b'\x01\x01\x01\x15\x01\r\x00\x00\x00\x00\xaa\xbb\xcc\xdd'
numeroPacote = 1
tipo2 = 2
totalPacotes = 21
tipo2, h0 = 2, tipo2.to_bytes(1, 'big')                            # tipo de mensagem
h1, h2, h6, h7, h8, h9 = 1, 1, 0, 0, 0, 0                                           # livre
h1, h2 = h1.to_bytes(1,'big'), h2.to_bytes(1, 'big')    # número total de pacotes no arquivos
totalPacotes, h3 = 21,  totalPacotes.to_bytes(1, 'big')                      # 
h4 = 1
h4 = h4.to_bytes(1, 'big')                            # número do pacote sendo enviado
h5 = rxBuffer[5].to_bytes(1, 'big') # id do arquivo                        # tipo handshake = id do arquivo, tipo dados = tamanho payload
h6 = h6.to_bytes(1, 'big')
h7 = numeroPacote                            # pacote solicitado quando tem erro
h7 = h7.to_bytes(1, 'big')                            # último pacote recebido com sucesso
h8 = h8.to_bytes(1, 'big')                            # CRC
h9 = h9.to_bytes(1, 'big') 
HEAD = [h0, h1, h2, h3, h4, h5, h6, h7, h8, h9]
EOP = [b'\xAA', b'\xBB', b'\xCC', b'\xDD']
pacote = HEAD + EOP
print(pacote, b''.join(pacote))
# txBuffer = b''.join(pacote)
# print(f"Enviando pacote de conferencia")