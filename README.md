# tic-tac-toe
ИИ Крестики-Нолики
Данный скрипт - первый эксперент по DQN сетям.
Итог пока следующий:
  1. Обучать игрой с рандомом не корректно. Каждый раз получается различный результат со смещением в какую-либо сторону.
  2. Лучшего результата удалось добиться сохранив все ходы в отдельный файл, после чего убрать из него все дубликаты и обучать уже на готовом наборе.

Требует дальнейшей доработки.
tic_tac_gui.py - Описание графического интерфейса игры
dqn.py - Описание сетки
tic_tac_dqn.py - Описание отношений первых двух )
file.py - Удаление дубликатов из файла
dqn_edu.py  -Обучение сети на готовом наборе

Что хотелось бы доработать:
  1. Разобраться с весами - чтобы сеть сильнее стремилась к победе
  2. Обучить играть первым игроком
  3. Поэксперементировать с составом сети.
  