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

endereco_completo = Endereco(
    "Rua 1", 
    11, 
    "Complemento 1", 
    "Bairro 1", 
    "Município 1", 
    "Estado 1", 
    "Cep 1"
)

loja_completa = Loja(
    "Loja 1",
    endereco_completo,
    "(11)1111-1111",
    "Observacao 1",
    "987654321",
    "123456789"
)

loja_com_erros = Loja(
    "",
    endereco_completo,
    "(11)1111-1111",
    "Observacao 1",
    "987654321",
    "123456789"
)

##

COO = "123456"
CCF = "123456"

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

produto_sample = Produto(
    0o1, 
    "Maçã", 
    "R$", 
    11.11, 
    "ST"
)

produto_gratuito = Produto(
    0o1, 
    "Maçã", 
    "R$", 
    0, 
    "ST"
)

item_sample = ItemVenda(
    1,
    produto_sample,
    2
)

##

venda_com_um_produto = Venda(
    loja_completa,
    CCF,
    COO,
    [item_sample]
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
        venda_com_um_produto,
        produto_sample,
        1
    )

def test_quantidade_menor_que_um():
    valida_item_adicionado(
        MSG_ERR_QUANTIDADE, 
        venda_sem_itens,
        produto_sample,
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