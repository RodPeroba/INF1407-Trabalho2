onload = function() {
    setupProduto();
};

function setupProduto() {
    const urlParams = new URLSearchParams(window.location.search);
    const produtoId = urlParams.get("produto");
    fetch(backendAddress + "/pgProduto/" + produtoId + "/", {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        },
        body: null,
        })
    .then((response) => response.json())
    .then((data) => {
        let produtoDiv = document.getElementById("detalhesProduto");
        let infoProduto = criaProdutoUnico(data);
        produtoDiv?.appendChild(infoProduto);
    })
    .catch((error) => {
        console.error("Erro ao carregar a página do produto:", error);
    });
}

function criaProdutoUnico(produto: any) {
  let itemProduto = document.createElement("ul");

  let nomeProduto = document.createElement("div");
  nomeProduto.appendChild(document.createTextNode("Produto: " + produto.nome));
  itemProduto.appendChild(nomeProduto);

  let precoProduto = document.createElement("div");
  precoProduto.appendChild(
    document.createTextNode("Preço: R$ " + produto.preco)
  );
  itemProduto.appendChild(precoProduto);

  let categoriaProduto = document.createElement("div");
  categoriaProduto.appendChild(
    document.createTextNode("Categoria: " + minhasCategorias[produto.categoria])
  );
  itemProduto.appendChild(categoriaProduto);

  let vendedorProduto = document.createElement("div");
  vendedorProduto.appendChild(
    document.createTextNode("Vendedor: " + produto.vendedor)
  );
  itemProduto.appendChild(vendedorProduto);

  let descricaoProduto = document.createElement("div");
  descricaoProduto.appendChild(
    document.createTextNode("Descrição: " + produto.descricao)
  );
  itemProduto.appendChild(descricaoProduto);

  let botaoComprar = document.createElement("button");
  botaoComprar.textContent = "Comprar agora";
  botaoComprar.addEventListener("click", function () {
    fetch(backendAddress + "/compraProduto/" + produto.id + "/", {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json",
        },
        body: null,
        })
    .then((response) => response.json())
    .then((data) => {
        alert("Compra realizada com sucesso!");     //TODO melhorar feedback para o usuário
        window.location.href = "index.html";
    })
    .catch((error) => {
        console.error("Erro ao realizar a compra:", error);
    });
  });
  itemProduto.appendChild(botaoComprar);

  return itemProduto;
}