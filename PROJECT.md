# A Link to the Past — macOS, Windows e visual diorama

Projeto de **Hiran Tiago Lins Borba** · Toronto, ON, CA
GitHub: https://github.com/htiagolborba
Autoria, contribuições e terceiros: [CREDITS.md](CREDITS.md).

## Objetivo
Manter as regras e conteúdo de A Link to the Past e desenvolver uma apresentação
com volumes arredondados, materiais de miniatura, iluminação suave e câmera de
diorama, inspirada na direção visual de Link’s Awakening para Switch.

## Estado em 25/10/2026
- ROM validada e recursos extraídos; ver rom-report.json.
- Base de reimplementação C: zelda3/ (snesrev/zelda3).
- CLT instalado e validado: Apple Clang 21.0.0, GNU Make 3.81, alvo x86_64.
- SDL2 2.32.10 compilado e instalado localmente em .tools/sdl2/.
- Jogo compilado com sucesso usando Clang e -Werror, como Mach-O x86_64.
- Vinculação estática do SDL2; otool confirma dependências dinâmicas do sistema.
- Aplicativo Zelda ALttP.app criado; abertura solicitada via open.
- Inspeção automática da janela expirou: título, áudio e controles ainda precisam
  de validação visual. O processo da primeira execução permaneceu ativo até
  ser encerrado deliberadamente para abrir a versão empacotada.
- Nenhuma alteração visual aplicada ao jogo nesta etapa.

## Decisão técnica inicial
A renderização atual passa por ZeldaDrawPpuFrame em src/zelda_rtl.c e entrega
um framebuffer ao backend em src/main.c. Ampliar PNGs ou aplicar um shader ao
framebuffer não cria geometria, sombras ou perspectiva reais. Os gráficos de
SNES usam tiles, paletas e limites próprios; PNGs maiores não são substitutos
diretos no fluxo existente.

Para buscar o visual pretendido, avaliar um renderer 3D/2.5D separado, alimentado
pelo estado da lógica C. Preservar a renderização original como referência.
O vínculo entre entidades, animações, mapas e geometria é trabalho de engenharia
novo; a base atual não fornece uma API de cena 3D pronta.

## Etapas e critérios
1. Ferramentas: concluir CLT, verificar clang/make/SDK, instalar SDL2.
2. Referência funcional: compilar a base original e validar entrada, áudio,
   saves e transições. Isso estabelece uma referência para detectar regressões.
3. Protótipo visual isolado: uma área pequena, câmera ortográfica inclinada,
   terreno, casa, árvores e personagem com proporções de miniatura. Usar recursos
   próprios e materiais simples antes de produzir o acervo completo.
4. Integração experimental: exportar estado de uma área e posição do personagem
   da lógica C; usar a cena para exibição mantendo colisões e regras originais.
   Validar oclusão, alturas, passagem por portas, animação e alinhamento espacial.
5. Fatia jogável: uma área externa e uma sala interna, movimento, espada,
   interação, transição e salvamento. Aprovar visual e desempenho nesta escala.
6. Expansão: ferramentas de conversão/autoria para mapas, personagens, inimigos,
   objetos, efeitos e interface. Só então ampliar para o jogo inteiro.
7. Distribuição local: bundle .app e testes na arquitetura alvo.

## Questões a resolver no protótipo
- Escolha entre renderer próprio e engine 3D, com base no custo de integrar a
  lógica C, ferramentas de cena, desempenho e empacotamento no macOS.
- Alvo inicial: Mac x86_64 observado neste ambiente; Apple Silicon requer teste.
- Preservar leitura clara de ataques e colisões ao mudar perspectiva e volumes.
- Profundidade de campo discreta para não prejudicar a leitura da área jogável.
- A ROM fornece dados e gráficos 2D, não modelos 3D de alta qualidade.

## Próxima verificação após concluir o instalador
xcode-select -p
xcrun --find clang
clang --version
make --version

Depois instalar SDL2 e executar ./build-macos.sh conforme README-macOS.md.

## Releases macOS e Windows — 25/10/2026

- Windows x86_64 compilado com LLVM-MinGW 20260616 e SDL2 2.32.10.
- Ícone Triforce e metadados de autoria incluídos no executável Windows.
- Comando --version adicionado à base para diagnóstico sem ROM.
- README.md em inglês criado para apresentação pública do projeto.
- Pacotes públicos separados por plataforma, sem ROM ou recursos extraídos.
- Ferramenta local de extração, checksums SHA-256 e manifesto por pacote.
- GitHub Actions preparado para build, verificação do loader no Windows e
  criação de dois releases em rascunho. Execução remota ainda pendente.
- Publicação depende da URL do repositório de destino.
- Testes reais de gameplay, áudio e controles físicos no Windows pendentes.
