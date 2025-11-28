"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
window.addEventListener("load", (evento) => {
    document.getElementById("formulario").addEventListener("click", (event) => __awaiter(void 0, void 0, void 0, function* () {
        event.preventDefault();
        const token = localStorage.getItem("token");
        const oldPassword = document.getElementById("old_password").value;
        const newPassword1 = document.getElementById("new_password1").value;
        const newPassword2 = document.getElementById("new_password2").value;
        if (newPassword1 !== newPassword2) {
            const msg = document.getElementById("msg");
            msg.textContent = "As novas senhas não coincidem.";
            return;
        }
        fetch(backendAddress + "contas/token-auth/", {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                Authorization: tokenKeyword + token,
            },
            body: JSON.stringify({
                old_password: document.getElementById("old_password").value,
                new_password: document.getElementById("new_password1").value,
            }),
        })
            .then((response) => {
            if (response.ok) {
                // Successful response, handle accordingly
                console.log("Senha trocada com sucesso!");
                return response.json();
            }
            else {
                // Error response, handle accordingly
                console.error("Erro ao trocar a senha: " + response);
                throw new Error("Erro ao trocar a senha: " + response);
            }
        })
            .then((data) => {
            const token = data.token;
            localStorage.setItem("token", token);
            //setLoggedUser();
            // 3 opções possíveis (e testadas)
            window.location.replace("passwordChangeDone.html");
        })
            .catch((error) => {
            // Network error or other exception
            console.error("Ocorreu um erro:", error);
        });
    }));
});
