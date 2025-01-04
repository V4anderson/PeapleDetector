Camera Motion Detection with Telegram Notifications

Este projeto implementa um script Python para monitoramento de vídeo em tempo real, detectando movimentações em uma região específica do vídeo capturado por uma câmera de segurança conectada a um DVR. Sempre que há movimento na área demarcada, o script envia uma notificação para o Telegram via API de Bot.

Tecnologias Utilizadas
Python: Linguagem de programação principal.
OpenCV (cv2): Biblioteca para processamento de vídeo e detecção de movimento.
Requests: Biblioteca para fazer requisições HTTP, usada para enviar notificações para o Telegram.
Telegram Bot API: API para enviar notificações para um canal ou chat no Telegram.
Funcionalidade
Monitoramento de Vídeo: O script monitora um stream de vídeo proveniente de uma câmera de segurança conectada a um DVR.
Detecção de Movimento: Ele verifica a movimentação em uma área específica da imagem capturada.
Notificação via Telegram: Quando detecta movimento, o script envia uma notificação para o Telegram, alertando o usuário.
Como Usar
Instalar o Python: Certifique-se de ter a última versão do Python instalada em sua máquina.

Instalar dependências: No diretório do projeto, execute o seguinte comando para instalar todas as dependências necessárias:


pip install -r requirements.txt
Configurar o Telegram Bot:

Crie um bot no Telegram através do BotFather e obtenha o token.
Obtenha o chat ID do grupo ou chat onde você deseja receber as notificações.
Configurar o Script:

Edite o script motion_detection.py para inserir o token do bot, o chat ID e a URL do stream de vídeo da sua câmera.
Executar o Script:


Copiar código
python motion_detection.py
Monitoramento em Tempo Real: O script começará a monitorar o vídeo e enviará uma notificação para o Telegram sempre que detectar movimento na área demarcada.
