onload = function(){
    setupAdicionarProduto();
}

function setupAdicionarProduto() {
    document.getElementById("submitProductButton")?.addEventListener("click", function(event) {
        // Prevenindo o comportamento padrão do formulário
        event.preventDefault();
        // Coletando os dados do formulário
        const elements = (document.getElementById("addProductForm") as HTMLFormElement).elements;
        let data: Record<string, string> = {};
        for (let i = 0; i < elements.length; i++) {
            const input = elements.item(i) as HTMLInputElement;
            data[input.name] = input.value;
        }
        data["vendedor"] = "1" //TODO pegar o id do vendedor logado
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
                (document.getElementById("message") as HTMLDivElement).innerText = "Produto adicionado com sucesso!";
            } else {
                (document.getElementById("message") as HTMLDivElement).innerText = "Erro ao adicionar produto.";
            }
        })
        
        .catch(error => {
            (document.getElementById("message") as HTMLDivElement).innerText = "Algum erro aconteceu";
        });
    });
}

