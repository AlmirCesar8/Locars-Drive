function pesquisar() {
  // Obtém a seção onde os resultados serão exibidos
  let section = document.getElementById("resultados-pesquisa");
  let campoPesquisa = document.getElementById("campo-pesquisa").value.toLowerCase();
  // Inicializa uma string vazia para armazenar os resultados
  let resultado = "";
  // Itera sobre cada dado na lista de dados
  for (let dado of dados) {
    let tag = dado.tags.toLowerCase()
    if (dado.nome.toLowerCase().includes(campoPesquisa) || dado.posicao.toLowerCase().includes(campoPesquisa) || dado.nacionalidade.toLowerCase().includes(campoPesquisa) || tag.includes(campoPesquisa)) {
      // Cria um novo elemento div para cada resultado
      if (dado.posicao != "goleiro") {
          resultado += `
          <div class="item-resultado">
            <div class="topo">
              <img class="perfil" src="jogadores/${dado.foto}" alt="${dado.nome}">
              <div class="info">
                  <h2>${dado.nome}<a href=${dado.insta} target="_blank"><img class="logo" src="imagens/insta.png" alt="Instagram"></a></h2>
                  <p>${dado.nacionalidade} de ${dado.idade} anos, o camisa ${dado.camisa} do Corinthians é um(a) ${dado.posicao} que já disputou ${dado.jogos} jogos, marcando ${dado.gols} gols e distribuindo ${dado.assistencias} assistências nessas partidas. ${dado.descricao}</p>
                  <a href="${dado.wiki}" target="_blank">Mais informações</a>
              </div>
            </div>
          </div>
          `;
        }
      else {
        resultado += `
        <div class="item-resultado">
          <div class="topo">
            <img class="perfil" src="jogadores/${dado.foto}" alt="${dado.nome}">
            <div class="info">
                <h2>${dado.nome}<a href=${dado.insta} target="_blank"><img class="logo" src="imagens/insta.png" alt="Instagram"></a></h2>
                <p>${dado.nacionalidade} de ${dado.idade} anos, o camisa ${dado.camisa} do Corinthians é um(a) ${dado.posicao} que já disputou ${dado.jogos} jogos, defendendo ${dado.penal_def} pênaltis e sofrendo ${dado.gols_sofri} gols. ${dado.descricao}</p>
                <a href="${dado.wiki}" target="_blank">Mais informações</a>
            </div>
          </div>
        </div>
        `;
      }
    }
  }
  if (!resultado) {
    resultado = '<div class= "item-erro"><h2>Nada foi encontrado</h2></div>';
  }
  // Atribui o HTML gerado à seção de resultados
  section.innerHTML = resultado;
}

// testes de funçoes para ordenar
// dados.sort().reverse();
// function ordenarGols(a,b){
//   return a.gols - b.gols;
// }
// function ordenarNome(a,b){
//   return a.nome - b.nome;
// }
// function ordenarAssistencias(a,b){
//   return a.assistencias - b.assistencias;
// }
// function ordenarIdade(a,b){
//   return a.idade - b.idade;
// }
// function ordenarTitulos(a,b){
//   return a.titulos - b.titulos;
// }