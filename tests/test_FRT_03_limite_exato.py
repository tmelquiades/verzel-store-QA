import re

import pytest
from playwright.sync_api import expect


@pytest.mark.ui
@pytest.mark.bug
def test_FRT_03_limite_exato(loja):
    """
    CT FRT-03 | CA06 | BUG-01
    Com subtotal exatamente em R$ 200,00, o frete deve ser grátis.

    ATENÇÃO: este teste FALHA enquanto o BUG-01 existir
    (hoje o carrinho cobra R$ 19,90 e exibe "Faltam R$ 0,00 para o frete grátis.").
    """
    # Dado que o carrinho tem P005 x2 (subtotal R$ 200,00)
    loja.adicionar_produto("Mochila Urbana 20L")
    loja.abrir_carrinho()
    loja.aumentar_quantidade()

    # Então o frete é grátis
    expect(
        loja.valor("frete"),
        "CA06: com subtotal de R$ 200,00 o frete deveria ser grátis (BUG-01)",
    ).to_have_text("Grátis")

    # E o total é R$ 200,00
    expect(loja.valor("total")).to_have_text(re.compile(r"200,00"))

    # E não há aviso de valor faltante para o frete grátis (CA07 só vale abaixo de R$ 200,00)
    expect(loja.page.get_by_text(re.compile(r"Faltam R\$"))).to_have_count(0)
