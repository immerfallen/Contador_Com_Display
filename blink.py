from machine import Pin, PWM
from time import sleep_ms

vermelho = Pin(16, Pin.OUT, value=0)
amarelo = Pin(17, Pin.OUT, value=0)
verde = Pin(18, Pin.OUT, value=1)
buzzer = PWM(Pin(14), freq=2000, duty_u16=0)

botao = Pin(15, Pin.IN, Pin.PULL_UP)

segmentos = {
    letra: Pin(gpio, Pin.OUT, value=0)
    for letra, gpio in zip("abcdefg", (2, 3, 4, 5, 6, 7, 8))
}

digitos = ("abcdef", "bc", "abdeg", "abcdg", "bcfg", "acdfg")


def escrever_display(acesos):
    for letra, pino in segmentos.items():
        pino.value(int(letra in acesos))


while True:
    if botao.value() == 0:
        sleep_ms(30)  # Confirma o aperto após o debounce.

        if botao.value() == 0:
            verde.off()
            amarelo.on()
            buzzer.duty_u16(32768)  # Começa o bip de 2 kHz.
            sleep_ms(1000)

            amarelo.off()

            buzzer.duty_u16(0)     # Silencia o buzzer.

            vermelho.on()

            for numero in range(5, 0, -1):
                escrever_display(digitos[numero])
                buzzer.duty_u16(32768)
                sleep_ms(150)
                buzzer.duty_u16(0)
                sleep_ms(850)

            for duracao in (100, 100, 100, 400):
                buzzer.duty_u16(32768)
                sleep_ms(duracao)
                buzzer.duty_u16(0)
                if duracao == 100:
                    sleep_ms(120)

            escrever_display("")  # Apaga todos os segmentos.
            vermelho.off()
            verde.on()

            # Aguarda a soltura para um botão segurado não repetir o ciclo.
            while True:
                if botao.value() == 1:
                    sleep_ms(30)
                    if botao.value() == 1:
                        break
                sleep_ms(10)

    sleep_ms(10)