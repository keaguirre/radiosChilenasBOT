import asyncio
import unittest
from unittest.mock import MagicMock
from bot import bot, transmitir, listar_radios, desconectar, detener_bot

class TestBotFunctions(unittest.TestCase):
    def test_transmitir(self):
        # Simula un contexto de Discord
        ctx = MagicMock()
        ctx.author.voice.channel = MagicMock()
        ctx.guild = MagicMock()

        # Llama a la función transmitir con un nombre de URL válido
        transmitir(ctx, "adn")

        # Verifica que se haya enviado un mensaje
        ctx.send.assert_called_once()

    def test_listar_radios(self):
        # Simula un contexto de Discord
        ctx = MagicMock()

        # Llama a la función listar_radios
        listar_radios(ctx)

        # Verifica que se haya enviado un mensaje
        ctx.send.assert_called_once()

    def test_desconectar(self):
        # Simula un contexto de Discord
        ctx = MagicMock()
        ctx.guild = MagicMock()

        # Llama a la función desconectar
        desconectar(ctx)

        # Verifica que se haya enviado un mensaje
        ctx.send.assert_called_once()
        
    def tearDown(self):
        # Llamamos a la función para detener el bot después de que las pruebas se hayan ejecutado
        asyncio.run(detener_bot(bot))

if __name__ == "__main__":
    unittest.main()
