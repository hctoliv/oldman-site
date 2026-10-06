# Old Man Sandwich Shop — site 2026

Site estático de página única. Sem build, sem dependências: abra `index.html`.

```bash
cd ~/Documents/oldman-site && python3 servidor.py
```

Use `servidor.py`, não o `python3 -m http.server`. O servidor padrão responde
HTTP/1.0 e ignora cabeçalho `Range`, e sem `Range` o Chrome não toca os MP4 do
site. Qualquer hospedagem estática de verdade já faz isso certo.

## Estrutura
- `index.html` — a home inteira (CSS e JS embutidos)
- `cardapio.html` — o cardápio completo, 35 itens
- `assets/img/` — fotos da marca e o logo recortado
- `assets/img/ig/` — miniaturas dos posts, nomeadas `NN-<id do post>.jpg`
- `assets/video/` — `legacy.mp4` (o reels do burger do mês) e o lugar do vídeo do hero
- `servidor.py` — servidor local com suporte a `Range`, necessário para o vídeo

## FALTAM DOIS ARQUIVOS

A página funciona sem eles, mas foi construída esperando os dois.

1. **`assets/video/hero.mp4`** — o vídeo de fundo do topo. Enquanto não existir,
   o hero mostra a foto do skatista como poster e nada quebra. Specs no
   `assets/video/LEIA-ME.txt`.
2. **Mais fotos de clientes.** O Instagram limita a API depois de poucas chamadas
   e o grid público trava em 12 posts, então só deu para pegar as que estavam ao
   alcance. O caminho para ter as outras é a pasta de fotos da produção.

## O vídeo do burger do mês

`assets/video/legacy.mp4` é o reels do Legacy, de setembro. Roda sozinho, mudo e
em loop, e só toca quando entra na tela (e pausa quando a aba sai de foco), para
não gastar bateria à toa.

Ele veio dos segmentos que o Instagram serve para o player, que são **VP9 dentro
de MP4** e o Chrome não toca de forma progressiva. Foi convertido para H.264 720p
com ffmpeg, que é o que funciona em todo navegador, inclusive no iPhone:

```bash
ffmpeg -i entrada.mp4 -an -vf scale=720:-2 -c:v libx264 -profile:v high \
  -pix_fmt yuv420p -crf 26 -preset slow -movflags +faststart saida.mp4
```

Quando trocar o burger do mês, troque o vídeo e o `poster` junto.

## O cardápio agora é o real

`cardapio.html` tem os 35 itens com os preços lidos direto da loja oficial no
iFood em 06/10/2026: burgers, chickens, entradas, a linha veg inteira, doces,
bebidas e cervejas. O layout segue a página de cardápio do Holy Burger: folha
de papel clara sobre o fundo escuro, moldura dupla, logo no topo e colunas com
o preço solto embaixo da descrição.

A home mostra cinco itens como vitrine e manda para a página completa.

**Isso envelhece.** Quando a cozinha mexer no cardápio ou no preço, os dois
arquivos precisam ser atualizados. A fonte é a loja no iFood.

## As imagens: como foram obtidas

O Instagram assina as URLs do CDN e elas expiram em cerca de um dia, então tudo
está salvo no repositório. As fotos em 1200 px (o skatista do hero) e a arte das
regras da casa em 1320 px vieram da sessão logada, passando por uma ponte local
em vez de download manual.

**O Instagram limita a API depois de poucas chamadas** (HTTP 429). O grid público
trava em 12 posts e a paginação parou de responder, então as fotos mais antigas
de clientes com o lanche não puderam ser coletadas. Para ter mais, o caminho é a
operação mandar a pasta de fotos da produção.

## De onde vieram os dados

Tudo saiu de fonte pública, porque a casa não tinha site. A base foi o próprio
Instagram (@oldmansandwich, perfil verificado, 90,6 mil seguidores em 06/10/2026).

| Dado | Fonte |
|---|---|
| Endereço, horário (18h às 23h30, todos os dias) e WhatsApp | Bio do Instagram |
| "2 vezes #1 no ranking do Guia do Hambúrguer" | Bio do Instagram |
| 2º lugar em 2026, 4 anos seguidos no pódio | Post da própria casa em 18/07/2026 |
| "Dirty hands is a sign of clean money" | Assinatura do mesmo post |
| Fundador Wendell Trevisan e a frase sobre servir | Reel do @wildsailors.studio, ago/2026 |
| Dona Margarida e a garagem | Comentário de cliente antigo no mesmo reel |
| "Garage Sandwich · Est. 2017 · Sem Reserva" | Placa da fachada |
| Sem reserva, grupos de até 6 pessoas | Post de 07/08/2026 (IPA Day) |
| Burgers do mês: Gasolina, Chicken Who?, Califa, Legacy | Posts de mai, jul, ago e set/2026 |
| Telefone (11) 4226-3712 | Guia do Hambúrguer e baressp |
| Nota 4,6 com mais de 7 mil avaliações | Agregadores (baressp, cardapio.menu) |
| Nota 4,9 no iFood e pedido mínimo de R$ 25 | Loja oficial no iFood, 06/10/2026 |
| Cardápio completo com preços | Loja oficial no iFood, 06/10/2026 |
| Arte "Regras da casa" com os personagens | Destaque INFOS do Instagram |
| Foto dos avós e da Dona Margarida | Posts de 12/06/2023 e 23/12/2023 |
| Indicação ao Prêmio Hambúrguer Perfeito | Post de 09/10/2024 |
| Foto do cliente de skate na porta | Post "Every single bite", 17/06/2026 |
| Foto da equipe com a placa | Post de 18/07/2026, original em 4096 px |

## Logo

É o logo oficial, não uma recriação em CSS. Veio da foto de perfil do Facebook
(389 px, a maior versão pública encontrada), recortado e convertido para PNG com
fundo transparente. O traço é branco, então funciona sobre qualquer fundo escuro.
Se a operação tiver o vetor, vale trocar por SVG: fica nítido em qualquer tamanho.

## Referências de direção

- **FÔRNO (fornosp.com.br)** — a parte suja: granulação, fotocópia de alto
  contraste, adesivo torto, borda rasgada.
- **Holy Burger (holyburger.com.br)** — a estrutura do topo: vídeo de fundo
  ocupando a tela inteira, escuro com dourado.
- **Sampa Burger** — o esqueleto da página, o status "aberto agora", o dock e o
  cardápio sem preço.

## Cores: saíram das fotos, não de chute

A paleta foi extraída das imagens da marca com k-means. As fotos são todas da
mesma família de matiz (17° a 37°), o que confirmou a direção:

- `--ink #0C0A08` — o preto da placa esmaltada e da foto de perfil
- `--bone #EFE8D2` — o branco do letreiro e da porcelana dos pratos
- `--gold #FBCA02` — o dourado de letrista da vitrine. Virou a cor de ação do site
- `--ember #CD7E2F` e `--brick #92451D` — a luz quente e o tijolo aparente

O site é escuro porque a marca é escura. A referência de estrutura foi o Sampa
Burger, mas a Sampa é clara com vermelho; aqui a base é preta com dourado.

## Onde cada foto está

- **Hero**: o cliente de skate comendo na porta. O título é a assinatura da casa,
  "Dirty hands is a sign of clean money", e embaixo "Carne na chapa, e pão tostado
  desde 2017". Nada de lista de prêmios no topo: isso está em Conquistas.

  O h1 ficou em inglês, então os termos de busca locais vivem no `<title>` e na
  meta description ("Hamburgueria artesanal em São Caetano do Sul"). Se um dia a
  busca por "hamburgueria são caetano" importar mais que a marca, é nesse par que
  se mexe, não no h1.
- **A casa**: a arte "Regras da casa", que fala exatamente do que a seção trata.
- **Burger do mês**: o reels do Legacy, rodando sozinho.
- **A história**: a Dona Margarida com o neto, porque a seção fala dela.
- **A vó**: o retrato dos avós em preto e branco.
- **Conquistas**: a equipe inteira em faixa larga, mais as duas do Prêmio
  Hambúrguer Perfeito.

`balcao.jpg`, `hero-vitrine.jpg` e `gasolina.jpg` ficaram no repositório sem uso,
disponíveis se alguma seção precisar trocar.

## Decisões

- **Preço só na página de cardápio**, com a data da conferência escrita embaixo.
  A home não mostra preço de tudo, só dos cinco em destaque.
- **A seção "A casa" existe por causa dos comentários.** Lendo os posts, as três
  dúvidas que mais aparecem são: tem no iFood, dá pra reservar e como funciona a
  fila. A seção responde as três antes da pessoa sair de casa.
- **O status "aberto agora"** recalcula no load, a cada minuto e quando a aba volta
  ao primeiro plano. Usa o fuso de São Paulo, não o relógio do visitante.
- **As imagens são emolduradas, não esticadas.** O Instagram entrega no máximo
  640 px para quem não está logado. Em vez de deformar, a foto aparece no tamanho
  que aguenta.
- **A revelação ao rolar tem rede de segurança.** Quem abre direto em `/#faq`
  pularia tudo que ficou para trás e esses blocos ficariam invisíveis para sempre.
  Uma varredura libera o que já passou pela dobra.
- **O tom é para o público da casa**: gente mais nova, sem rodeio e sem
  linguagem institucional. Sem travessão e sem frase de efeito vazia.
- **A página não é limpa de propósito.** Granulação por cima de tudo, fotos do
  Instagram em preto e branco estourado que só ganham cor no hover, adesivos
  tortos e borda rasgada entre seções. A marca é placa esmaltada e tijolo, não
  vitrine de shopping.

## A área de Instagram é um retrato, não um feed ao vivo

As miniaturas foram baixadas do perfil público em 06/10/2026 e ficam no repositório.
Isso foi de propósito: a URL que o Instagram serve no CDN é assinada e expira em
cerca de um dia, então apontar direto para lá quebraria o site sozinho.

Cada tile leva para o post real. Para atualizar, baixe as novas miniaturas em
`assets/img/ig/` e troque os blocos `<a class="ig-tile">`.

## Conferir com a operação antes de publicar

1. **Horário.** A bio do Instagram diz 18h às 23h30 todos os dias, e é isso que o
   site mostra. Mas a loja no iFood anuncia abertura às 11h30. Ou o delivery abre
   antes do salão, ou um dos dois está desatualizado. **Confirmar qual vale.**
2. **A nota 4,6 com 7.423 avaliações** veio de agregador, que aparenta espelhar o
   Google. Confirmar no perfil do Google antes de publicar, ou tirar o número.
3. **O burger do mês está travado no Legacy, de setembro.** Até 06/10/2026 o de
   outubro não tinha sido postado. Essa seção precisa de alguém trocando todo mês
   (texto, vídeo e poster), ou vira informação velha. Vale combinar quem faz.
7. **Conquistas.** O site diz "quatro anos seguidos no pódio, dois deles em
   primeiro lugar", que é o que a casa escreveu. **Quais anos foram os de primeiro
   lugar não está em lugar nenhum**, então a linha do tempo não afirma. Se a
   operação souber, dá para deixar mais forte.
4. **Fotos em alta.** O hero e as fotos do skatista estão em 1200 px; o resto do
   acervo ainda é de 640 px. Com os originais da produção o site ganha bastante.
5. **O link do iFood** foi pego de busca pública. Abrir uma vez e confirmar que é
   a loja certa.
6. **Não há domínio.** `oldmansandwich.com.br` aparece no Restaurant Guru como site
   oficial, mas o domínio não resolve. Checar se a casa tem o registro.

## O que a página de propósito não tem

- Reserva ou fila online. Os comentários mostram que a fila paga foi retirada e
  gerou atrito; a página só informa a regra, não vende uma solução que não existe.
- Preços, por serem voláteis.
- Formulário de cadastro. Sem alguém para responder, formulário só gera frustração.
