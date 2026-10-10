import re

import pytest
from playwright.sync_api import Page


class Loja:
    """Ações reutilizáveis da interface da Verzel Store."""

    def __init__(self, page: Page):
        self.page = page

    def abrir(self):
        self.page.goto("/")  # usa o base_url do pytest.ini

    def adicionar_produto(self, nome: str):
        self.page.get_by_role("article", name=nome).get_by_role("button").click()

    def abrir_carrinho(self):
        self.page.get_by_role("link", name=re.compile(r"^Carrinho")).click()

    def aumentar_quantidade(self, vezes: int = 1, forcar: bool = False):
        """Clica em "+" uma vez por iteração (mais confiável que click_count).

        forcar=True ignora a checagem de "botão habilitado": serve para tentar
        passar do limite tanto se o botão ficar desabilitado quanto se não ficar.
        """
        botao = self.page.get_by_role("button", name="Aumentar quantidade de")
        for _ in range(vezes):
            botao.click(force=forcar)

    def valor(self, nome: str):
        """Valor do resumo do pedido: 'subtotal', 'desconto', 'frete' ou 'total'."""
        return self.page.locator(f"[data-valor='{nome}']")


@pytest.fixture
def loja(page: Page) -> Loja:
    loja = Loja(page)
    loja.abrir()
    return loja
