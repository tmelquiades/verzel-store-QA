import re

import pytest
from playwright.sync_api import expect


@pytest.mark.ui
def test_UI_01_finalizar_compra(loja):
    """
    CT UI-01
    Finalizar a compra sem etapa de pagamento online (o pagamento é na entrega).
    """
    page = loja.page

    # Dado que o carrinho tem um produto e vou finalizar a compra
    loja.adicionar_produto("Calça Jeans Slim")
    loja.abrir_carrinho()
    page.get_by_role("link", name="Finalizar compra").click()

    # Então não existe etapa de pagamento online (nenhum campo de cartão)
    expect(page.get_by_label(re.compile(r"cart[aã]o|cvv", re.I))).to_have_count(0)

    # Quando preencho os dados do cliente e confirmo o pedido
    page.get_by_role("textbox", name="Nome completo").fill("Maria Silva")
    page.get_by_role("textbox", name="E-mail").fill("maria@exemplo.com")
    page.get_by_role("textbox", name="CEP").fill("01310100")
    page.get_by_role("button", name="Confirmar pedido").click()

    # Então o pedido é confirmado com número no formato VZ-000000
    expect(page.get_by_text("Pedido confirmado")).to_be_visible()
    expect(page.get_by_text(re.compile(r"VZ-\d{6}")).first).to_be_visible()
