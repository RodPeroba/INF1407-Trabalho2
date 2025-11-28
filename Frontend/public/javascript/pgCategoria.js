"use strict";
onload = function () {
    setupCategoria();
};
function setupCategoria() {
    const urlParams = new URLSearchParams(window.location.search);
    const categoria = urlParams.get("categoria");
    fetch(backendAddress + "/pgCategoria/" + categoria + "/", {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        },
    })
        .then((response) => response.json())
        .then((data) => {
        // Setup do HTML da homepage
        let container = document.createElement("div");
        let barraSuperior = document.createElement("div");
        let colunaEsquerda = document.createElement("div");
        let colunaDireita = document.createElement("div");
        let rodape = document.createElement("div");
        container.className = "container";
        barraSuperior.className = "barra-superior";
        colunaEsquerda.className = "coluna-esquerda";
        colunaDireita.className = "coluna-direita";
        rodape.className = "rodape";
        document.body.appendChild(container);
        container.appendChild(barraSuperior);
        container.appendChild(colunaEsquerda);
        container.appendChild(colunaDireita);
        container.appendChild(rodape);
        // Populando o HTML da homepage com os dados recebidos
        // Barra Superior
        let titulo = document.createElement("h1");
        titulo.textContent = `Bem-vindo à Loja - Categoria: ${minhasCategorias[data.categoria]} `;
        barraSuperior.appendChild(titulo);
        // Coluna Esquerda
        let categorias = document.createElement("h2");
        categorias.appendChild(document.createTextNode("Categorias"));
        colunaEsquerda.appendChild(categorias);
        let listaCategorias = document.createElement("ul");
        colunaEsquerda.appendChild(listaCategorias);
        for (let categoria of data.categorias) {
            let itemCategoria = document.createElement("li");
            let linkCategoria = document.createElement("a");
            const chaveCategoria = getCategoriaChave(categoria);
            linkCategoria.setAttribute("href", `pgCategoria.html?categoria=${chaveCategoria}`);
            linkCategoria.textContent = categoria;
            itemCategoria.appendChild(linkCategoria);
            listaCategorias.appendChild(itemCategoria);
        }
        // Coluna Direita
        let produtos = document.createElement("h2");
        produtos.appendChild(document.createTextNode("Todos os Produtos"));
        colunaDireita.appendChild(produtos);
        colunaDireita.appendChild(document.createElement("hr"));
        let listaProdutos = document.createElement("ul");
        colunaDireita.appendChild(listaProdutos);
        for (let produto of data.produtos) {
            let itemProduto = criaProdutoDaCategoria(produto);
            listaProdutos.appendChild(itemProduto);
        }
        // Rodapé
        rodape.appendChild(document.createTextNode("© 2025 Minha Loja Online"));
    })
        .catch((error) => {
        console.error("Error fetching categories:", error);
    });
}
function criaProdutoDaCategoria(produto) {
    let itemProduto = document.createElement("ul");
    let nomeProduto = document.createElement("div");
    nomeProduto.appendChild(document.createTextNode("Produto: " + produto.nome));
    itemProduto.appendChild(nomeProduto);
    let precoProduto = document.createElement("div");
    precoProduto.appendChild(document.createTextNode("Preço: R$ " + produto.preco));
    itemProduto.appendChild(precoProduto);
    let categoriaProduto = document.createElement("div");
    categoriaProduto.appendChild(document.createTextNode("Categoria: " + minhasCategorias[produto.categoria]));
    itemProduto.appendChild(categoriaProduto);
    let vendedorProduto = document.createElement("div");
    vendedorProduto.appendChild(document.createTextNode("Vendedor: " + produto.vendedor));
    itemProduto.appendChild(vendedorProduto);
    let descricaoProduto = document.createElement("div");
    descricaoProduto.appendChild(document.createTextNode("Descrição: " + produto.descricao));
    itemProduto.appendChild(descricaoProduto);
    let botaoComprar = document.createElement("button");
    botaoComprar.textContent = "Ver produto";
    botaoComprar.addEventListener("click", function () {
        window.location.href = `pgProduto.html?produto=${produto.id}`;
    });
    itemProduto.appendChild(botaoComprar);
    itemProduto.appendChild(document.createElement("hr"));
    return itemProduto;
}
