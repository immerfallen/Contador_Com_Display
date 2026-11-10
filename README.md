# Semáforo de pedestres com Raspberry Pi Pico

Protótipo em MicroPython com três LEDs, um botão, um display de 7 segmentos e um buzzer. O botão inicia um ciclo de travessia com contagem regressiva e sinal sonoro.

## Materiais

- Raspberry Pi Pico original com MicroPython e cabo micro-USB de dados
- LEDs vermelho, amarelo e verde, botão momentâneo e buzzer piezo passivo compatível com 3,3 V
- Display HS-5101AS de um dígito e cátodo comum
- Protoboard, jumpers e resistores em série com os LEDs

## Montagem

Desconecte o Pico do USB antes de montar. Use um GND comum para o circuito.

| Componente | GPIO | Pino físico do Pico | Ligação |
| --- | --- | ---: | --- |
| LED vermelho | GP16 | 21 | GPIO → resistor → ânodo. Cátodo → GND. |
| LED amarelo | GP17 | 22 | GPIO → resistor → ânodo. Cátodo → GND. |
| LED verde | GP18 | 24 | GPIO → resistor → ânodo. Cátodo → GND. |
| Buzzer passivo | GP14 | 19 | Terminal positivo no GPIO e negativo no GND. |
| Botão | GP15 | 20 | Um terminal no GPIO e o outro no GND. |

Na montagem testada, o verde ficou mais brilhante com 220 Ω. Use um resistor por LED. O botão usa o pull-up interno e é lido como 0 quando pressionado.

### Display HS-5101AS

Use um resistor de 330 Ω em série **por segmento**. Confira a orientação no [datasheet do 5101AS](https://www.xlitx.com/datasheet/5101AS.pdf) antes de contar os pinos.

| Segmento | Pino do display | GPIO | Pino físico do Pico |
| --- | ---: | --- | ---: |
| A | 7 | GP2 | 4 |
| B | 6 | GP3 | 5 |
| C | 4 | GP4 | 6 |
| D | 2 | GP5 | 7 |
| E | 1 | GP6 | 9 |
| F | 9 | GP7 | 10 |
| G | 10 | GP8 | 11 |
| Cátodo comum | 3 e 8 | GND | 8, por exemplo |
| Ponto decimal | 5 | Livre | — |

## Como rodar

1. Conecte o Pico com MicroPython ao computador.
2. Abra a pasta `Contador_Com_Display` como raiz no VS Code com a extensão MicroPico.
3. Abra [blink.py](blink.py), use **MicroPico: Connect** e depois **MicroPico: Run Current File on Board** na paleta de comandos.
4. Confirme que o verde acende e o display fica apagado. Aperte o botão para iniciar o ciclo.

## Sequência do semáforo

1. O verde fica aceso até o programa confirmar o aperto do botão com uma segunda leitura após 30 ms.
2. O amarelo acende por 1 segundo com um tom de 2 kHz.
3. No vermelho, o display mostra **5 → 4 → 3 → 2 → 1**. Cada número fica visível por 1 segundo, com um bip de 150 ms seguido de 850 ms de silêncio.
4. Ainda no vermelho, o buzzer toca três bipes de 100 ms, cada um seguido de 120 ms de silêncio, e um bip final de 400 ms.
5. O display apaga e o verde volta. O programa aguarda a soltura do botão antes de aceitar um novo pedido.

## Como o código funciona

O dicionário `segmentos` associa as letras A–G às saídas do Pico. A tupla `digitos` guarda as barras que formam cada número. Por exemplo, `digitos[1]` contém `"bc"`, as duas barras da direita. A função `escrever_display()` percorre todos os segmentos e liga só os presentes no texto recebido. Uma string vazia apaga o visor.

O buzzer usa PWM a 2 kHz. `duty_u16(32768)` gera o tom com cerca de 50% de ciclo ativo e `duty_u16(0)` silencia a saída. Os `sleep_ms()` controlam a duração das fases. Enquanto a travessia está em andamento, o programa não consulta o botão.
