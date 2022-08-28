# Тестовое упражнение: разбор почтового лога и поиск записей по адресу получателя.

## Описание задания
Подробное описание задания приведено в файле [Task-1.pdf](./Task-1.pdf).

## Решение задания.

### SQL
Установленная у меня MariaDB 10.6 не приняла команды создания таблиц из задания. Исправленный
код приведён в файле [tblcreate.sql](./tblcreate.sql). Таблицы должны быть созданы в
базе данных 'test'.
```shell
mysql test < tblcreate.sql
```

### Парсер лога.
Скрипт парсера - файл [prsr](./prsr).
Скрипт запускается командой './prsr <имя файла>' или подачей файла/потока на стандартный ввод.
Например:
```shell
./prsr out
./prsr < out
```

### Поиск записей.
Поиск записей осуществляется с помощью генератора web-страниц [log.cgi](./log.cgi), который необходимо
разместить в папке /cgi-bin/ сервера, на котором работает СУБД, содержащая базу test.
При первом обращении по адресу http://server-addr/cgi-bin/log.cgi отображается
форма с полем ввода почтового адреса реципиента. При заполнении поля и отправке запроса,
выводятся записи журнала, относящиеся к этому реципиенту. Выводится не более 100 записей,
что можно поменять изменением переменной LINELIMIT в теле log.cgi.
