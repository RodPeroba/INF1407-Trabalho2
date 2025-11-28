"use strict";
onload = () => {
    document.getElementById('btnCriarConta').addEventListener('click', evento => {
        evento.preventDefault();
        const username = document.getElementById('username');
        const password = document.getElementById('password');
        const confirmPassword = document.getElementById('confirmPassword');
        const email = document.getElementById('email');
        const group = document.getElementById('group');
        const msg = document.getElementById('msg');
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
            }
            else {
                msg.appendChild(document.createTextNode('Erro ao criar conta.'));
            }
        }).catch(error => {
            msg.appendChild(document.createTextNode('Erro ao criar conta.'));
        });
    });
};
