# Slavinator
### Will help you

Бот был создан для выполнения заданий по бухгалтерскому учету

По входным данным (проводкам и начальному балансу), алгоритм посчитает и визуализирует синтетические счета (самолетики), путем стилизации границ и отступов, а также создаст оборотно-сальдовую ведомость.

Телеграмм выступает в качестве GUI (пользовательского интерфейса)

## How it work
<article>
  Необходимо нажать на соответсвующию инлайн кнопку и бот будет готов принимать данные
  
  Данные нужно передать внутри файла excel в специальном формате:
  <p>
    1-я колонка начальные данные {Номер счета} {Сальдо начальное}
  </p>
  <p>
    2-я колонка Сами проводки в формате {Дебет} {Кредит} {Сумма} с пробелами
  </p>
</article>
<div id="header" align="center">
  <img src="https://i.imgur.com/DHSJ7eq.gif" width="800"/>
</div>


### How to Start - NEED TO CREATE YOURSELF TELEGRAM BOT
1. git clone https://github.com/fklska/Slavinator
2. python -m venv venv | sourse venv activate
3. run main.py
