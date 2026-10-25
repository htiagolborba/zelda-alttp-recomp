# Zelda: A Link to the Past — preparação para macOS

Projeto de **Hiran Tiago Lins Borba** · Toronto, ON, CA
GitHub: https://github.com/htiagolborba
Autoria, contribuições e terceiros: [CREDITS.md](CREDITS.md).

## Estado

ROM americana, revisão 0, LoROM, sem cabeçalho de copiador: 1.048.576 bytes (1 MiB).
SRAM: 8 KiB. Checksum calculado e informado: 0xAF0D; complemento válido.
SHA-256: `66871d66be19ad2c34c927d6b14cd8eb6fc3181965b6e517cb361f7316009cfb`.
Detalhes e hash do pacote extraído: `rom-report.json`.

O código em `zelda3/` vem de https://github.com/snesrev/zelda3 (licença em
`zelda3/LICENSE.txt`). É uma reimplementação da lógica do jogo em C com
componentes PPU/DSP de SNES; não é uma tradução automática do código 65C816.
O código-fonte original da Nintendo não é recuperado pela extração.

## Conteúdo extraído

- `zelda3/zelda3_assets.dat`: pacote de execução, 683.888 bytes.
- `zelda3/assets/`: gráficos PNG, diálogos e tabelas de texto.
- `zelda3/assets/overworld/`: mapas externos em YAML.
- `zelda3/assets/dungeon/`: salas e dados de dungeons em YAML.
- `zelda3/assets/sound/`: recursos de áudio.

A ROM original e o ZIP em `backup/` foram preservados. Existe uma cópia em
`zelda3/zelda3.sfc` para o extrator. A dependência PyYAML foi instalada apenas
em `.tools/python/`. Os recursos extraídos permanecem locais.

## Compilação nativa

O ambiente é macOS x86_64. CLT validado (Apple Clang 21 e Make 3.81).
SDL2 2.32.10 foi compilado da fonte oficial e instalado em `.tools/sdl2/`,
sem Homebrew. A compilação do jogo terminou com sucesso usando `-Werror`.
O único aviso na vinculação foi uma biblioteca matemática `-lm` repetida.

Abra `Zelda ALttP.app` pelo Finder. O aplicativo contém o executável, recursos
e configuração inicial. Saves e configuração do aplicativo são gravados em
`~/Library/Application Support/Zelda ALttP/`. O aplicativo é uma build local,
sem assinatura Developer ID ou notarização. Não foi testado em Apple Silicon.
A abertura foi solicitada, mas a inspeção automática da janela expirou;
a validação visual, do áudio, dos controles e dos saves continua pendente.

Para recompilar o executável: `./build-macos.sh`.
Para executar pelo terminal: `cd zelda3 && ./zelda3`.
A recompilação não atualiza automaticamente a cópia dentro do `.app`.

O script usa o pacote de recursos já gerado. Para refazer a extração neste
ambiente, use na pasta `zelda3/`:

```sh
PYTHONPATH=../.tools/python /Users/hiranborba/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 assets/restool.py --extract-from-rom
```

Após compilar, valide abertura, áudio, controles, saves e transições de salas.
O projeto também oferece comparação por frame com a ROM; consulte o README
upstream antes de usar esse modo. Empacotamento `.app` e testes em Apple Silicon
ficam para a próxima etapa, após a compilação básica funcionar.
