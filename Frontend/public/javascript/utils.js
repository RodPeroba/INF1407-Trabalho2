"use strict";
function getCategoriaChave(nomeCategoria) {
    return Object.keys(minhasCategorias).find((key) => minhasCategorias[key] === nomeCategoria);
}
