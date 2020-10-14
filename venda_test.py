from cupom import get_data_hora
from cupom import Venda, Endereco, Loja, ItemVenda, Produto
import pytest

##

def verifica_campo_obrigatorio_venda(mensagem_esperada, venda):
    with pytest.raises(Exception) as excinfo:
        venda.dados_venda()
    the_exception = excinfo.value
    assert mensagem_esperada == str(the_exception)

##

def valida_item_adicionado(
    mensagem_esperada, 
    venda,
    produto,
    quantidade
):
    with pytest.raises(Exception) as excinfo:
        venda.adicionar_item(produto,quantidade)
    the_exception = excinfo.value
    assert mensagem_esperada == str(the_exception)

##

def valida_impressao(mensagem_esperada, venda):
    with pytest.raises(Exception) as excinfo:
        venda.imprimir_cupom()
    the_exception = excinfo.value
    assert mensagem_esperada == str(the_exception)

##

# @Endereco
LOGRADOURO = "Rua 1"
NUMERO = 11
COMPLEMENTO = "Complemento 1"
BAIRRO = "Bairro 1"
MUNICIPIO = "Município 1"
ESTADO = "Estado 1"
CEP = "11111-111"

# @Loja
NOME_LOJA = "Loja 1"
TELEFONE = "(11)1111-1111"
OBSERVACAO = "Observacao 1"
CNPJ = "987654321"
INSCRICAO_ESTADUAL = "123456789"

# @Venda
DATA_HORA = "11/11/11 11:11:11V"
CCF = "123456"
COO = "123456"

QUANTIDADE = QTD = 2
UNIDADE= UND = "R$"
SUBSTITUICAO_TRIBUTARIA = ST = "ST" 

# @Produto produto1
CODIGO1 = "001"
DESCRICAO1 = "Maçã"
VALOR_UNITARIO1 = VU1 = 1.11

# @Produto produto2
CODIGO2 = "002"
DESCRICAO2 = "Banana"
VALOR_UNITARIO2 = VU2 = 2

endereco_completo = Endereco(
    LOGRADOURO, 
    NUMERO, 
    COMPLEMENTO, 
    BAIRRO, 
    MUNICIPIO, 
    ESTADO, 
    CEP
)

loja_completa = Loja(
    NOME_LOJA,
    endereco_completo,
    TELEFONE,
    OBSERVACAO,
    CNPJ,
    INSCRICAO_ESTADUAL
)

loja_com_erros = Loja(
    "",
    endereco_completo,
    TELEFONE,
    OBSERVACAO,
    CNPJ,
    INSCRICAO_ESTADUAL
)

##

venda_sem_itens = Venda(
    loja_completa,
    CCF,
    COO
)

venda_com_loja_irregular = Venda(
    loja_com_erros,
    CCF,
    COO
)

venda_com_ccf_invalido = Venda(
    loja_completa,
    "12345",
    COO
)

venda_com_coo_invalido = Venda(
    loja_completa,
    CCF,
    "12345"
)

venda_com_ccf_vazio = Venda(
    loja_completa,
    "",
    COO
)

venda_com_coo_vazio = Venda(
    loja_completa,
    CCF,
    ""
)

##

produto1_sample = Produto(
    CODIGO1, 
    DESCRICAO1, 
    UNIDADE, 
    VALOR_UNITARIO1, 
    SUBSTITUICAO_TRIBUTARIA
)

produto2_sample = Produto(
    CODIGO2, 
    DESCRICAO2, 
    UNIDADE, 
    VALOR_UNITARIO2, 
    SUBSTITUICAO_TRIBUTARIA
)

produto_gratuito = Produto(
    CODIGO1, 
    DESCRICAO1, 
    UNIDADE, 
    0, 
    SUBSTITUICAO_TRIBUTARIA
)

item1_sample = ItemVenda(
    1,
    produto1_sample,
    QUANTIDADE
)

item2_sample = ItemVenda(
    2,
    produto2_sample,
    QUANTIDADE
)

##

venda_com_produtos = Venda(
    loja_completa,
    CCF,
    COO,
    [item1_sample, item2_sample]
)

##

def only_one(text):
    lista = (
        f"{list(range(10))}"
          .strip("[]")
          .replace(",", " ")
          .split()
    )
    new_text = ""
    for char in text:
        if char in lista:
            new_text += "1"
        else:
            new_text += char
    return new_text

##

def test_data_hora():
    data_homogenea = only_one(get_data_hora())
    assert data_homogenea == "11/11/1111 11:11:11V"

##

MSG_ERR_LOJA_INVALIDA = "Loja é um campo obrigatório. Insira uma loja válida."
MSG_ERR_CCF_INVALIDO = "O CCF inserido não é válido."
MSG_ERR_COO_INVALIDO  = "O COO inserido não é válido."
MSG_ERR_CCF  = "O Contador de Cupom Fiscal (CCF) é obrigatório."
MSG_ERR_COO  = "O Contador de Ordem de Operação (COO) é obrigatório."

def test_valida_loja():
    verifica_campo_obrigatorio_venda(MSG_ERR_LOJA_INVALIDA, venda_com_loja_irregular)

def test_valida_ccf():
    verifica_campo_obrigatorio_venda(MSG_ERR_CCF, venda_com_ccf_vazio)
    verifica_campo_obrigatorio_venda(MSG_ERR_CCF_INVALIDO, venda_com_ccf_invalido)

def test_valida_coo():
    verifica_campo_obrigatorio_venda(MSG_ERR_COO, venda_com_coo_vazio)
    verifica_campo_obrigatorio_venda(MSG_ERR_COO_INVALIDO, venda_com_coo_invalido)

def test_valida_coo():
    verifica_campo_obrigatorio_venda(MSG_ERR_COO, venda_com_coo_vazio)
    verifica_campo_obrigatorio_venda(MSG_ERR_COO_INVALIDO, venda_com_coo_invalido)

##

MSG_ERR_SEM_ITENS = "Não há itens para imprimir."
MSG_ERR_ITEM_DUPLICADO = "O produto já está na lista."
MSG_ERR_QUANTIDADE = "Item de Venda com quantidade zero ou negativa."
MSG_ERR_VALOR_VENDA = "Produto com valor unitário zero ou negativo."

def test_sem_itens():
    valida_impressao(MSG_ERR_SEM_ITENS, venda_sem_itens)

def test_item_duplicado():
    valida_item_adicionado(
        MSG_ERR_ITEM_DUPLICADO, 
        venda_com_produtos,
        produto1_sample,
        1
    )

def test_quantidade_menor_que_um():
    valida_item_adicionado(
        MSG_ERR_QUANTIDADE, 
        venda_sem_itens,
        produto1_sample,
        0
    )

def test_valor_irrelevante():
    valida_item_adicionado(
        MSG_ERR_VALOR_VENDA, 
        venda_sem_itens,
        produto_gratuito,
        1
    )

##

venda_com_produtos_datahora_sample = Venda(
    loja_completa,
    CCF,
    COO,
    [item1_sample, item2_sample],
    "11/11/11 11:11:11V"
)

HIFENS = "-" * 30

TEXTO_ESPERADO_CUPOM_FISCAL_DOIS_ITENS = \
f"""{NOME_LOJA}
{LOGRADOURO}, {NUMERO} {COMPLEMENTO}
{BAIRRO} - {MUNICIPIO} - {ESTADO}
CEP:{CEP} Tel {TELEFONE}
{OBSERVACAO}
CNPJ: {CNPJ}
IE: {INSCRICAO_ESTADUAL}
{HIFENS} 
11/11/11 11:11:11V CCF:{CCF} COO:{COO}
     CUPOM FISCAL     
ITEM CODIGO DESCRICAO QTD UN VL UNIT(R$) ST VL ITEM(R$)
1 {CODIGO1} {DESCRICAO1} {QTD} {UNIDADE} {VU1:.2f} {ST} {VU1*QTD:.2f}
2 {CODIGO2} {DESCRICAO2} {QTD} {UNIDADE} {VU2:.2f} {ST} {VU2*QTD:.2f}
------------------------------
TOTAL: R$ 6.22"""

def test_impressao_cupom():
    assert venda_com_produtos_datahora_sample.imprimir_cupom() == \
    TEXTO_ESPERADO_CUPOM_FISCAL_DOIS_ITENS