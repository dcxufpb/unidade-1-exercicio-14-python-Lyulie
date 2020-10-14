# coding: utf-8

class Endereco:
  
  def __init__(self, logradouro, numero, complemento, bairro, municipio, 
      estado, cep):
    self.logradouro = logradouro
    self.numero = numero
    self.complemento = complemento
    self.bairro = bairro
    self.municipio = municipio
    self.estado = estado
    self.cep = cep
  
  def dados_endereco(self):

    self.validar_campos_obrigatorios()

    _logradouro = self.logradouro + ", "
    _numero = self.numero and str(self.numero) or "s/n"
    _complemento = self.complemento and " " + self.complemento or ""

    _bairro = self.bairro and self.bairro + " - " or ""
    _municipio = self.municipio + " - "

    _cep = self.cep and ("CEP:" + self.cep) or ""

    return \
f"""{_logradouro}{_numero}{_complemento}
{_bairro}{_municipio}{self.estado}
{_cep}"""

  def validar_campos_obrigatorios(self):
    if not self.logradouro:
      raise Exception ("O campo logradouro do endereço é obrigatório")

    if not self.municipio:
      raise Exception ("O campo município do endereço é obrigatório")

    if not self.estado:
      raise Exception ("O campo estado do endereço é obrigatório")

######

class Loja:
  
  def __init__(self, nome_loja, endereco, telefone, observacao, cnpj, 
      inscricao_estadual):
    self.nome_loja = nome_loja
    self.endereco = endereco
    self.telefone = telefone
    self.observacao = observacao
    self.cnpj = cnpj
    self.inscricao_estadual = inscricao_estadual

  def dados_loja(self):

    self.validar_campos_obrigatorios()

    _telefone = self.telefone and ("Tel " + self.telefone) or ""
    _telefone = (_telefone and self.endereco.cep) and (" " + _telefone) or _telefone

    _observacao = self.observacao and self.observacao or ""

    _cnpj = "CNPJ: " + self.cnpj
    _inscricao_estadual = "IE: " + self.inscricao_estadual
    
    return \
f"""{self.nome_loja}
{self.endereco.dados_endereco()}{_telefone}
{_observacao}
{_cnpj}
{_inscricao_estadual}"""

  def validar_campos_obrigatorios(self):
    if not self.nome_loja:
      raise Exception ("O campo nome da loja é obrigatório")

    if not self.cnpj:
      raise Exception ("O campo CNPJ da loja é obrigatório")

    if not self.inscricao_estadual:
      raise Exception ("O campo inscrição estadual da loja é obrigatório")

######

class Produto:
  def __init__ (
    self, 
    codigo, 
    descricao, 
    unidade, 
    valor_unitario, 
    substituicao_tributaria
  ):
    self.codigo = codigo 
    self.descricao = descricao
    self.unidade = unidade
    self.valor_unitario = valor_unitario
    self.substituicao_tributaria = substituicao_tributaria

######

class ItemVenda:
  def __init__ (
    self,
    item,
    produto,
    quantidade
  ):
    self.item = item
    self.produto = produto
    self.quantidade = quantidade
  
  def valor_total(self) -> float:
    return self.quantidade * self.produto.valor_unitario

  def dados_item(self) -> str:

    output = f"{self.item} {self.produto.codigo} {self.produto.descricao} "
    output += f"{self.quantidade} {self.produto.unidade} {self.produto.valor_unitario:.2f} "
    output += f"{self.produto.substituicao_tributaria} {self.valor_total():.2f}"
    return output

from datetime import datetime

def get_data_hora() -> str:
  data = datetime.now()
  data_format = data.strftime('%d/%m/%Y %H:%M:%S')
  return data_format + "V"

######

class Venda:

  def __init__ (
    self,
    loja,
    ccf,
    coo,
    itens = [],
    datahora = get_data_hora()
  ):
    self.loja = loja
    self.ccf = ccf
    self.coo = coo
    self.datahora = datahora
    self.itens = itens

  ##

  def calcular_total(self):
    total = 0
    for item in self.itens:
      total += item.valor_total()
    return total

  ##

  def validar_campos_obrigatorios(self) -> any:
    if not self.coo:
      raise Exception("O Contador de Ordem de Operação (COO) é obrigatório.")
    
    elif(len(self.coo) != 6):
      raise Exception("O COO inserido não é válido.")
    
    if not self.ccf:
      raise Exception("O Contador de Cupom Fiscal (CCF) é obrigatório.")
    
    elif(len(self.ccf) != 6):
      raise Exception("O CCF inserido não é válido.")

    try:
      self.loja.dados_loja()
    except:
      raise Exception("Loja é um campo obrigatório. Insira uma loja válida.")
  
  ##

  def is_duplicado(self, codigo) -> bool:
    for item in self.itens:
      if item.produto.codigo == codigo:
        return True
    return False

  ##

  def validar_item_adicionado(
    self, 
    produto, 
    quantidade
  ) -> any:
    if produto.valor_unitario <= 0:
      raise Exception ("Produto com valor unitário zero ou negativo.")

    if quantidade <= 0:
      raise Exception ("Item de Venda com quantidade zero ou negativa.")

    if self.is_duplicado(produto.codigo):
      raise Exception ("O produto já está na lista.")
  
  ##
  
  def adicionar_item(
    self, 
    produto, 
    quantidade
  ) -> any:
    self.validar_item_adicionado(produto, quantidade)

    item = len(self.itens) + 1
    item_para_add = ItemVenda(item, produto, quantidade)
    self.itens.append(item_para_add)

  ##

  def dados_venda(self) -> str:
    self.validar_campos_obrigatorios()

    return f"{self.datahora} CCF:{self.ccf} COO:{self.coo}"
    
  ##

  def dados_itens(self) -> str:
    stringfy = ""
    for item in self.itens:
      if stringfy == "":
        stringfy += item.dados_item()
      else:
        stringfy += "\n" + item.dados_item()

    return 'ITEM CODIGO DESCRICAO QTD UN VL UNIT(R$) ST VL ITEM(R$)\n' + stringfy
  
  ##

  def imprimir_cupom(self) -> str:
    if len(self.itens) == 0:
      raise Exception ("Não há itens para imprimir.")

    dados_loja = self.loja.dados_loja()
    dados_venda = self.dados_venda()
    dados_itens = self.dados_itens()

    hifens = "-" * 30
    
    return (
f"""{dados_loja}
{hifens} 
{dados_venda}
     CUPOM FISCAL     
{dados_itens}
{hifens}
TOTAL: R$ {self.calcular_total():.2f}"""
    )