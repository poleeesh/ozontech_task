# ozontech_task

## 10 Основных проблем кода (от самых критичных до самых неважных)

### 1) Нет очищения файлов

Если мы запустим этот тест на каждой существующей в программе породе, или будем перезапускать тест по несколько раз, наша тестовая папка в Яндекс Диске будет заспамлена кучей картинок, в итоге тест сломается и начнёт проверять всех, надо добавить очищение папки после окончания теста

### 2) Непонятное и неправильное обозначение фикстуры

Мало того, что она обозначена просто одной буквой, что противоречит общественным правилам написания кода, она ещё присутствует в самом тесте перед комментарием со словом "проверка". В пайтесте уже давно придуманы фикстуры, пусть мы вынесем её, а в тесте должен находиться код который действительно тестирует

### 3) Невынесенные константы

Все константы для удобства необходимо вынести в начало файла и брать их оттуда, в тесте много раз создаются переменные с одними и теми же ссылками, а если бы у нас был целый набор тестов на 500 строк, и ссылки поменялись, мы бы тогда рылись в коде меняя каждую ссылку? Зачем усложнять так жизнь если раз и навсегда можно сделать одну константную переменную и менять её (токен по-хорошему вообще надо вынести в отдельный конфиг файл)

### 4) Отсутствие типизации функций

Было бы намного понятнее для читателей кода сделать типизацию аргументов, передающихся функциям и что функции возвращают, тогда не нужно создавать переменные, которые не будут использоваться (типа response/resp в функциях YandexUploader), так как понятно, что эти функции ничего не возвращают поэтому результаты их внутренних функций post/put никуда записывать не надо

### 5) Непонятное строение класса YaUploader

Зачем там инит, если ничего не инитится? Зачем тогда создавать объект класса а потом запускать его функции, если мы можем сделать их статическими и запускать сразу (либо второй вариант, поставить в инит класса аттрибуты ссылки на яндекс диск и заголовка, и сделать эти методы классовыми)

### 6) Тест без тест-сьюта

Если мы будем расширять тестирование этой программы, лучше всё объединить в один тест-сьют созданием класса с тестами, в него же нужно поместить и фикстуру для загрузки картинок, так сразу будет понятнее что фикстура используется только для тестов внутри этого класса

### 7) Дублирующийся код

Очень много дублирующегося кода, возникающего за счёт невынесенных констант, одинаковых действий и в if ветке и в else ветке и постоянного получения айтемов из response.json(), когда их можно сразу вынести в отдельную переменную, если мы к ним не единожды обращаемся

### 8) Функции использующие DogCeo без класса

Очевидно, что как и для аплоадера в яндекс диск, для получения информации из DogCeo API также будет удобнее создать отдельный класс для обозначения общего сервиса, с которым работают функции

### 9) Ненужные конструкции

В коде есть ненужные конструкции типа assert True, ненужный цикл в тесте, так как там проверяется как раз перед ним что в списке всего одна вещь, можно упростить if get_sub_breeds(breed) == [] в if not get_sub_breeds(breed)

### 10) Нет allure

Чтобы сразу сгенерить красивый отчётик можно использовать allure в коде
