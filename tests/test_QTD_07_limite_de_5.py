import re

import pytest
from playwright.sync_api import expect


@pytest.mark.ui
def test_QTD_07_limite_de_5(loja):
    """
    CT QTD-07 | CA10
    Cada produto pode ter no máximo 5 unidades por pedido na interface.
    """
    # Dado que o carrinho tem P001 x5 (5 x R$ 59,90 = R$ 299,50)
    loja.adicionar_produto("Camiseta Essencial")
    loja.abrir_carrinho()
    loja.aumentar_quantidade(vezes=4)
    expect(loja.valor("subtotal")).to_have_text(re.compile(r"299,50"))

    # Quando tento adicionar mais uma unidade
    loja.aumentar_quantidade(forcar=True)

    # Então a mensagem de limite é exibida
    expect(loja.page.get_by_text("Limite de 5 unidades por")).to_be_visible()

    # E a quantidade não passa de 5 (o subtotal permanece R$ 299,50)
    expect(loja.valor("subtotal")).to_have_text(re.compile(r"299,50"))
