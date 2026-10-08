# Breakout - Jogo Arcade com Pipeline Gráfico Próprio

Um jogo de **Breakout** 2D desenvolvido em **Pygame** para a disciplina de Computação Gráfica. O jogador controla uma raquete para rebater a bola e destruir todos os tijolos, enquanto a câmera pode aproximar, afastar e acompanhar a bola.

 _(Feito por Yan de Freitas)_

---

## Sobre o Projeto

O objetivo principal do trabalho foi explorar a implementação de lógica de jogo, física e renderização usando apenas os recursos fundamentais do Pygame. Diferente de jogos que usam sprites e funções de desenho prontas, todo o desenho é feito **pixel a pixel** por um **pipeline gráfico próprio**: rasterização de primitivas, preenchimento de regiões, transformações geométricas, janela/viewport e recorte foram implementados do zero.

O Pygame é usado apenas para criar a janela, ler teclado e mouse, exibir a imagem final e carregar arquivos de imagem. As únicas exceções são a limpeza de quadro com `Surface.fill` e o texto, gerado com `pygame.font`.

## Demonstração

_Arquivo do vídeo: [Breakout](https://github.com/Yan-Freitas/https---github.com-Yan-Freitas-trabalho_CompGrafica/blob/main/assets/Breakout.mp4))_

### Estrutura de Pastas

```text
trabalho_CompGrafica/
├── lib/                        # Biblioteca gráfica
│   ├── Motor_grafico.py        # setPixel com recorte de segurança
│   ├── Primitivas.py           # Bresenham, polígonos, círculo e elipse
│   ├── Preenchimento.py        # Boundary Fill, scanline, gradiente e textura
│   ├── Recorte.py              # Algoritmo de Cohen-Sutherland
│   ├── Transformacoes.py       # Matrizes 3x3 e álgebra linear
│   └── Viewport.py             # Mapeamento janela -> viewport
├── jogo/                       # O jogo em si
│   ├── config.py               # Constantes (tamanhos, cores, velocidades)
│   ├── geometria.py            # Transformações em torno de um pivô
│   ├── entidades.py            # Raquete, Bola e Tijolo (polígonos)
│   ├── fisica.py               # Colisões e reflexão
│   ├── janela.py               # Janela de mundo (zoom e deslocamento)
│   ├── partida.py              # Regras, estado e entrada do jogo
│   ├── renderizador.py         # Pipeline mundo -> tela
│   ├── abertura.py             # Tela de abertura
│   ├── menu.py                 # Menu interativo
│   └── fonte.py                # Texto com pygame.font
├── assets/
│   └── paddle.png              # Textura da raquete (opcional)
└── main.py                     # Loop principal e integração
```

### Principais Funcionalidades

O grande destaque do projeto é que ele **não usa as funções de desenho padrão do Pygame**. Em vez disso, foi construído um pipeline gráfico que processa a renderização pixel a pixel. Para começar, o código foi dividido em partes, uma para cada funcionalidade.

**Pasta `lib`**

* `Motor_grafico.py`

A função base `setPixel` foi implementada com um sistema de **recorte de segurança**: ela verifica os limites da superfície antes de escrever, garantindo que o motor gráfico nunca tente acessar coordenadas fora da janela.

* `Primitivas.py`

As formas geométricas são processadas por algoritmos clássicos de Computação Gráfica:

* **Bresenham (retas):** implementação só com aritmética inteira, tratando todos os octantes, usada para a grade do cenário, as bordas do campo e as linhas da abertura.
* **Polígonos:** `desenhar_poligono` liga os vértices com Bresenham (usado no contorno dos tijolos da abertura), e `desenhar_poligono_recortado` aplica o Cohen-Sutherland em cada aresta.
* **Ponto médio (círculos e elipses):** `desenhar_circulo` e `desenhar_elipse` usam o algoritmo do ponto médio e preenchem o interior em faixas horizontais. São usadas na tela de abertura.

* `Preenchimento.py`

* **Boundary Fill (baseado em pilha):** para regiões irregulares, o preenchimento usa uma pilha em vez de recursão, evitando o estouro de pilha (*Stack Overflow*) comum nas versões recursivas. É usado para pintar os tijolos da tela de abertura.
* **Scanline:** `scanline_fill` encontra as interseções do polígono em cada linha da tela e preenche entre elas, sem falhas entre os pixels.
* **Interpolação de cores (gradientes):** `scanline_fill_gradiente` interpola linearmente as cores definidas por vértice, ao longo das arestas e depois ao longo de cada linha. É usada nos tijolos, na bola e nos botões do menu.
* **Mapeamento de textura (UV):** `scanline_texture` projeta coordenadas (U, V) em polígonos arbitrários e respeita o canal alfa da imagem. É usada na raquete.

* `Recorte.py`

O algoritmo de **Cohen-Sutherland** divide o espaço em 9 regiões com códigos binários (esquerda, direita, abaixo e acima).

* **Desempenho:** testes lógicos rápidos aceitam ou rejeitam a reta sem calcular interseções quando possível.
* **Precisão:** o recorte é feito matematicamente antes de enviar os pixels para a função de desenho, evitando rasterização desnecessária.

* `Transformacoes.py`

O movimento e a forma dos objetos são processados por matrizes de transformação:

* **Coordenadas homogêneas:** matrizes 3×3 para translação, rotação (em graus) e escala de forma unificada.
* **Composição de matrizes:** `multiplica_matrizes` permite combinar transformações e aplicá-las aos polígonos de uma só vez com `aplica_transformacao`.

* `Viewport.py`

`janela_viewport(janela, viewport)` devolve a matriz que leva coordenadas do mundo (janela) para a tela (viewport), composta por translação, escala e translação (`T(V) · S · T(-W)`). Isso separa o mundo lógico das coordenadas da tela, e a mesma função alimenta duas viewports (a principal e o minimapa).

**Pasta `jogo`**

* `entidades.py`

Nada no jogo usa sprites: a raquete, a bola e os tijolos são **polígonos** definidos em coordenadas locais e levados ao mundo por transformações.

* **Raquete:** retângulo escalado e transladado, preenchido com **textura** de imagem.
* **Bola:** polígono de 12 lados com gradiente vertical simples (cores claras nos vértices de cima e escuras nos de baixo), posicionado por **translação**.
* **Tijolo:** quatro vértices com gradiente (claro em cima, escuro embaixo). Ao ser atingido, ele **encolhe e gira** por 0,3 s antes de sumir.

* `geometria.py`

Como as matrizes de `Transformacoes.py` não têm pivô, este módulo monta escala e rotação em torno de um ponto compondo `T(c) · M · T(-c)`. Ele é o único ponto do jogo que conversa com `Transformacoes.py`.

* `janela.py`

A janela de mundo define o que a câmera enxerga:

* **Zoom dinâmico:** é uma **escala** dos cantos da janela em torno do centro (teclas Z e X), de 1× até 4×.
* **Câmera livre:** o deslocamento é uma **translação** da janela (teclas I, J, K, L), sempre limitada ao mundo.
* **Câmera que segue a bola:** com a tecla F, a janela se aproxima suavemente da posição da bola.

* `renderizador.py`

Aqui o pipeline completo se encontra: cada objeto passa por **mundo → recorte → matriz janela→viewport → rasterização**.

* **Retas** (grade, bordas do campo e retângulo do minimapa) são recortadas com **Cohen-Sutherland** contra a janela antes de serem desenhadas.
* **Polígonos** fora da viewport são descartados antes do preenchimento, o que mantém o desempenho com zoom.
* **Duas viewports:** a principal mostra o jogo de perto, e o **minimapa** mostra o mundo inteiro, com um retângulo amarelo indicando a área vista pela câmera principal. Ele reutiliza as mesmas funções de polígono e preenchimento.
* Cada viewport usa o `set_clip` da superfície para o desenho de uma não vazar para a outra.

* `fisica.py` e `partida.py`

* **Colisão círculo × retângulo:** calculada pelo ponto mais próximo do retângulo, com normal para a reflexão da velocidade.
* **Rebatida na raquete:** o ângulo de saída depende do ponto de impacto (até 60° para cada lado).
* **Ângulo mínimo:** depois de bater em um tijolo, a bola nunca fica quase horizontal (|vy| ≥ 25% da velocidade).
* **Subpassos:** cada quadro é dividido em passos menores, para a bola não atravessar objetos em quadros lentos.
* **Estados:** pronta para lançar, jogando, pausada, fim de jogo e vitória. O jogador tem 3 vidas.

* `abertura.py`

A tela de abertura é estática: todas as formas são desenhadas de uma só vez, com as primitivas da `lib`. Os tijolos têm o contorno feito por `desenhar_poligono` e o interior pintado por **Boundary Fill**; o chão e a trajetória usam **Bresenham**; a bola é uma **circunferência** (`desenhar_circulo`) e a raquete é uma **elipse** (`desenhar_elipse`). O texto "PRESSIONE ENTER" pisca.

* `menu.py`

Menu interativo controlado por teclado ou mouse, com as opções JOGAR, DIFICULDADE (Fácil, Normal e Difícil, que mudam a velocidade da bola) e SAIR. O botão selecionado pulsa por meio de uma transformação de escala.

* `fonte.py`

O texto é gerado com `font.render` e copiado com `blit` direto na tela, depois que o framebuffer é exibido. Os módulos pedem o texto com `agendar_texto`, e o `main.py` escreve a fila com `desenhar_fila(tela)`.

**`main.py`**

É onde tudo o que foi construído nas outras pastas se conecta para formar a experiência do jogo.

* **Framebuffer próprio:** todo o desenho é feito em uma superfície auxiliar com `setPixel`, que depois é exibida na janela. A superfície é travada (`lock`) durante o desenho para o acesso pixel a pixel ficar mais rápido.
* **Máquina de estados:** abertura → menu → jogo, com retorno ao menu pela tecla Esc.
* **Tempo real:** o movimento usa o tempo entre quadros (`dt`), então a velocidade do jogo não depende do FPS.
* **Textura:** `carregar_textura` lê `assets/paddle.png`. Se o arquivo não existir, gera uma textura quadriculada com `setPixel`.

## Controles

| Tecla | Ação |
|---|---|
| ← / → | Move a raquete |
| Espaço | Lança a bola |
| Z / X | Aumenta / diminui o zoom da janela |
| I / J / K / L | Move a janela (cima / esquerda / baixo / direita) |
| F | Liga/desliga a janela seguindo a bola |
| C | Reseta a janela (zoom 1×) |
| P | Pausa |
| R | Reinicia (após fim de jogo ou vitória) |
| Esc | Volta ao menu |

**Menu:** ↑/↓ (ou W/S) para navegar, Enter/Espaço para escolher, ←/→ para trocar a dificuldade. Também funciona com o mouse (passar o cursor e clicar).

## Requisitos do Trabalho × Onde Estão

| Requisito | Implementação |
|---|---|
| Set Pixel | `lib/Motor_grafico.py` |
| Reta, círculo e elipse | `bresenham`, `desenhar_poligono`, `desenhar_circulo` e `desenhar_elipse` em `lib/Primitivas.py`, usados em `jogo/abertura.py` |
| Flood Fill / Boundary Fill | `boundary_fill` em `lib/Preenchimento.py`, usado nos tijolos da abertura |
| Scanline | `scanline_fill` (minimapa, mensagens) |
| Gradiente por vértice | `scanline_fill_gradiente` (tijolos, bola, botões) |
| Textura de imagem | `scanline_texture` (raquete) |
| Translação, escala e rotação | `lib/Transformacoes.py` via `jogo/geometria.py` |
| Animação 2D | Tijolo encolhe e gira ao ser atingido; botão do menu pulsa; texto da abertura pisca; movimento da bola e da raquete |
| Janela e viewport | `jogo/janela.py` (zoom e deslocamento) e `lib/Viewport.py` (principal e minimapa) |
| Cohen-Sutherland | `lib/Recorte.py`, aplicado em `Renderizador.linha` |
| Teclado e mouse | Teclado no jogo; teclado e mouse no menu |
| Menu | `jogo/menu.py` |

## Linguagem e Bibliotecas

* Python 3
* Pygame

### Pré-requisitos

É necessário ter o Python 3.10 ou superior instalado (testado com 3.12). Para instalar a biblioteca usada, execute:

```bash
pip install pygame
```

### Como executar o Breakout

Depois de instalar a biblioteca, abra o terminal na **raiz do projeto** e execute:

```bash
python main.py
```

> Execute sempre a partir da raiz do repositório, porque os imports usam as pastas `lib` e `jogo`.

### Textura da raquete

Coloque uma imagem PNG (sugestão: 64×32, com canal alfa) em `assets/paddle.png`. Sem ela, o jogo usa a textura quadriculada de reserva.

### Desempenho

Todo o preenchimento é feito em Python, pixel a pixel, então o jogo roda em torno de 10 a 20 quadros por segundo, dependendo do computador. Para ganhar velocidade, reduza `BRICK_ROWS`, `BRICK_COLS` ou o tamanho dos tijolos em `jogo/config.py`.
