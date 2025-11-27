"use strict";
onload = function () {
    setupAdicionarProduto();
};
function setupAdicionarProduto() {
    var _a;
    (_a = document.getElementById("submitProductButton")) === null || _a === void 0 ? void 0 : _a.addEventListener("click", function (event) {
        // Prevenindo o comportamento padrão do formulário
        event.preventDefault();
        // Coletando os dados do formulário
        const elements = document.getElementById("addProductForm").elements;
        let data = {};
        for (let i = 0; i < elements.length; i++) {
            const input = elements.item(i);
            data[input.name] = input.value;
        }
        data["vendedor"] = "1"; //TODO pegar o id do vendedor logado
        //Enviando os dados para o backend
        fetch(backendAddress + "/vendedor/cadastro_produto/", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
            .then(response => {
            if (response.ok) {
                document.getElementById("message").innerText = "Produto adicionado com sucesso!";
            }
            else {
                document.getElementById("message").innerText = "Erro ao adicionar produto.";
            }
        })
            .catch(error => {
            document.getElementById("message").innerText = "Algum erro aconteceu";
        });
    });
}
