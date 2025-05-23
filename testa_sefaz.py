from zeep import Client
from zeep.transports import Transport
import requests

# WSDL da SEFAZ Nacional (exemplo para ambiente de homologação)
wsdl = 'https://homologacao.nfe.sefazvirtual.rs.gov.br/ws/NfeStatusServico/NfeStatusServico2.asmx?wsdl'

# Crie o cliente SOAP
session = requests.Session()
client = Client(wsdl=wsdl, transport=Transport(session=session))

# Monta o XML de consulta de status
xml = '''
<consStatServ versao="4.00" xmlns="http://www.portalfiscal.inf.br/nfe">
  <tpAmb>2</tpAmb>
  <cUF>35</cUF>
  <xServ>STATUS</xServ>
</consStatServ>
'''

# Chama o serviço
response = client.service.nfeStatusServicoNF2(xml)
print(response)