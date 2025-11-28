function getCategoriaChave(nomeCategoria: any): string | undefined {
  return Object.keys(minhasCategorias).find(
    (key) => minhasCategorias[key] === nomeCategoria
  );
}
