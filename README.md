# Projeto Django: Lembretes & Notas (skeleton)

Este projeto contém um esqueleto Django com app `notes` que implementa:
- Modelo `Note` (owner, title, content, is_public, public_token)
- Modelo `Reminder` ligado a `Note`
- Views de listagem, criação, edição, deleção, página pública por token
- Template base com usuário logado e link de logout/login
- Management command `send_reminders` para envio de notificações (console/email)
- Arquivos estáticos (styles.css)

Instruções rápidas:
1. Crie e ative um virtualenv.
2. `pip install django`
3. Copie a pasta `lembretes_project` para o local do seu projeto.
4. `python manage.py migrate`
5. `python manage.py createsuperuser`
6. `python manage.py runserver`
7. (opcional) Teste o comando: `python manage.py send_reminders`

Notas:
- O backend de email por padrão usa console (ver settings.py) para facilitar testes.
- Ajuste SECRET_KEY e DEBUG conforme necessário antes de produção.
