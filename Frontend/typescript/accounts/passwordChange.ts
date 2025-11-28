window.addEventListener("load", (evento) => {
  (document.getElementById("formulario") as HTMLFormElement).addEventListener(
    "click",
    async (event) => {
      event.preventDefault();
      const token = localStorage.getItem("token");
      const oldPassword = (
        document.getElementById("old_password") as HTMLInputElement
      ).value;
      const newPassword1 = (
        document.getElementById("new_password1") as HTMLInputElement
      ).value;
      const newPassword2 = (
        document.getElementById("new_password2") as HTMLInputElement
      ).value;
      if (newPassword1 !== newPassword2) {
        const msg = (document.getElementById("msg") as HTMLDivElement);
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
          old_password: (
            document.getElementById("old_password") as HTMLInputElement
          ).value,
          new_password: (
            document.getElementById("new_password1") as HTMLInputElement
          ).value,
        }),
      })
        .then((response: Response) => {
          if (response.ok) {
            // Successful response, handle accordingly
            console.log("Senha trocada com sucesso!");
            return response.json();
          } else {
            // Error response, handle accordingly
            console.error("Erro ao trocar a senha: " + response);
            throw new Error("Erro ao trocar a senha: " + response);
          }
        })
        .then((data: { token: string }) => {
          const token: string = data.token;
          localStorage.setItem("token", token);
          //setLoggedUser();
          // 3 opções possíveis (e testadas)
          window.location.replace("passwordChangeDone.html");
        })
        .catch((error) => {
          // Network error or other exception
          console.error("Ocorreu um erro:", error);
        });
    }
  );
});
