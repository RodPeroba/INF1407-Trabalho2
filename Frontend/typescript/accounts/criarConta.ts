onload = () => {
    (document.getElementById('btnCriarConta') as HTMLInputElement).addEventListener('click', evento => {
        evento.preventDefault();
        const username: HTMLInputElement = (document.getElementById('username') as HTMLInputElement);
        const password: HTMLInputElement = (document.getElementById('password') as HTMLInputElement);
        const confirmPassword: HTMLInputElement = (document.getElementById('confirmPassword') as HTMLInputElement);
        const email: HTMLInputElement = (document.getElementById('email') as HTMLInputElement);
        const group: HTMLInputElement = (document.getElementById('group') as HTMLInputElement);
        const msg = (document.getElementById('msg') as HTMLDivElement);
        if (password.value !== confirmPassword.value) {
            msg.appendChild(document.createTextNode('As senhas não coincidem.'));
            return;
        }
        fetch(backendAddress + 'contas/create-account/', {
            method: 'POST',
            body: JSON.stringify({
                username: username.value,
                password: password.value,
                email: email.value,
                group: group.value
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(response => {
            if (response.ok) {
                msg.appendChild(document.createTextNode('Conta criada com sucesso.'));
                username.value = '';
                password.value = '';
                confirmPassword.value = '';
                email.value = '';
                group.value = '';
            } else {
                msg.appendChild(document.createTextNode('Erro ao criar conta.'));
            }
        }).catch(error => {
            msg.appendChild(document.createTextNode('Erro ao criar conta.'));
        });
    });
}