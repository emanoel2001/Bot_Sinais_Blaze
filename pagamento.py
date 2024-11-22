import crcmod
import qrcode


class Payload():
    def __init__(self, nome, chavepix, valor, cidade, txtId):
        self.nome = nome
        self.chavepix = chavepix
        self.valor = valor
        self.cidade = cidade
        self.txtId = txtId

        self.nome_tam = len(self.nome)
        self.chavepix_tam = len(self.chavepix)
        self.valor_tam = len(valor)
        self.cidade_tam = len(cidade)
        self.txtId_tam = len(txtId)

        self.merchantAccount_tam = f'0014br.gov.bcb.pix01{
            self.chavepix_tam}{self.chavepix}'

        self.payloadFormat = "000201"

        self.merchantAccount = f"26{len(self.merchantAccount_tam)}{
            self.merchantAccount_tam}"

        if self.valor_tam <= 9:
            self.transactionAmount_tam = f"0{self.valor_tam}{self.valor}"
        else:
            self.transactionAmount_tam = f"{self.valor_tam}{self.valor}"

        if self.txtId_tam <= 9:
            self.addDateField_tam = f"050{self.txtId_tam}{self.txtId}"
        else:
            self.addDateField_tam = f"05{self.txtId_tam}{self.txtId}"

        if self.nome_tam <= 9:
            self.nome_tam = f"0{self.nome_tam}"

        if self.cidade_tam <= 9:
            self.cidade_tam = f"0{self.cidade_tam}"

        self.merchantCategCod = '52040000'

        self.transactionCurrency = '5303986'

        self.transactionAmount = f'54{self.transactionAmount_tam}'

        self.countryCode = '5802BR'

        self.merchantName = f'59{self.nome_tam}{self.nome}'

        self.merchantCity = f'60{self.cidade_tam}{self.cidade}'

        self.addDataField = f'62{len(self.addDateField_tam)}{
            self.addDateField_tam}'

        self.crc16 = '6304'

    def gerarPayload(self):
        self.payload = f"{self.payloadFormat}{self.merchantAccount}{self.merchantCategCod}{self.transactionCurrency}{self.transactionAmount}{self.countryCode}{self.merchantName}{self.merchantCity}{self.addDataField}{self.crc16}"

        print()
        print(self.payload)
        print()

        self.gerar_crc16(self.payload)

    def gerar_crc16(self, payload):
        crc16 = crcmod.mkCrcFun(
            poly=0x11021, initCrc=0xFFFF, rev=False, xorOut=0x0000)

        self.crc16Code = hex(crc16(str(payload).encode('utf-8')))

        self.crc16Code_formatado = str(
            self.crc16Code).replace('0x', '').upper()

        self.payload_completa = f"{payload}{self.crc16Code_formatado}"

        print()
        print(self.payload_completa)
        print()

        self.gerarQrCode(self.payload_completa)

    def gerarQrCode(self, payload):
        self.qrcode = qrcode.make(payload)
        self.qrcode.save('pixqrcode.png')