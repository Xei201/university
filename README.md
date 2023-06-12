# Задание для кандидата на должность Junior Python Developer
### Задачи
1. База данных.
2. SQL запросы.
3. FastAPI.
4. Публикация и документация.

## Часть 1: База данных

Ваша задача - создать ER-диаграмму (схему связей между сущностями) и определить свойства каждой из этих сущностей. 
Затем напишите SQL запросы для создания соответствующих таблиц, включающих все необходимые поля и связи между ними.

### ER-диаграммa
![ER-диаграммa](https://github.com/Xei201/university/blob/master/img/ER-diagram.png)

### SQL запросы для создания соответствующих таблиц

В качестве БД я использовал PostgreSQL, все инструкции далее приводятся в рамках работы с ней.
Необходимо запустить SQL Shell (psql). Программа предложит ввести название сервера, базы данных, порта и пользователя. 
Эти пункты можно прощелкать, так как для них будут использоваться значения по умолчанию 
(для сервера - localhost, для базы данных - postgres, для порта - 5432, в качестве пользователя - суперпользователь postres). 
Далее надо будет ввести пароль для пользователя (по умолчанию пользователя postgres)

Создаём базу данных:
```js
create database university;
```
Далее подключимся к этой базе данных:
```js
\c university;
```
Используем SQL скрипт ниже для создания всех зависимостей:
```js
CREATE TABLE faculty_type(
    name VARCHAR(50) PRIMARY KEY
);


CREATE TABLE faculty(
    faculty_id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(50) NOT NULL);


CREATE TABLE course(
    course_id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(50) NOT NULL
);


CREATE TABLE semester(
    semester_id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    start_date TIMESTAMP DEFAULT NULL,
    end_date TIMESTAMP DEFAULT NULL
);


CREATE TABLE building(
    building_number INT PRIMARY KEY,
    address VARCHAR(50)
);


CREATE TABLE audience(
    audience_number INT PRIMARY KEY,
    building_number INT,
    FOREIGN KEY(building_number)
        REFERENCES building(building_number)
        ON DELETE CASCADE
);


CREATE TABLE group_student(
    group_id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(50) NOT NULL,
    faculty_id INT,
    faculty_type VARCHAR(50),
    FOREIGN KEY(faculty_id)
        REFERENCES faculty(faculty_id)
        ON DELETE SET NULL,
    FOREIGN KEY(faculty_type)
        REFERENCES faculty_type(name)
        ON DELETE SET NULL
);


CREATE TABLE student(
    student_id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    group_id INT,
    FOREIGN KEY(group_id)
        REFERENCES group_student(group_id)
        ON DELETE SET NULL
);


CREATE TABLE teacher(
    teacher_id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    faculty_id INT,
    FOREIGN KEY(faculty_id)
        REFERENCES faculty(faculty_id)
        ON DELETE SET NULL
);


CREATE TABLE syllabus(
    syllabus_id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    faculty_id INT,
    semester_id INT,
    course_id INT,
    FOREIGN KEY(faculty_id)
        REFERENCES faculty(faculty_id)
        ON DELETE CASCADE,
    FOREIGN KEY(semester_id)
        REFERENCES semester(semester_id)
        ON DELETE CASCADE,
    FOREIGN KEY(course_id)
        REFERENCES course(course_id)
        ON DELETE CASCADE
);




CREATE TABLE course_program(
    program_id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(50) NOT NULL,
    course_id INT,
    teacher_id INT,
    FOREIGN KEY(course_id)
        REFERENCES course(course_id)
        ON DELETE CASCADE,
    FOREIGN KEY(teacher_id)
        REFERENCES teacher(teacher_id)
        ON DELETE SET NULL
);


CREATE TABLE program_student(
    program_student_id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    student_id INT,
    program_id INT,
    FOREIGN KEY(student_id)
        REFERENCES student(student_id)
        ON DELETE CASCADE,
    FOREIGN KEY(program_id)
        REFERENCES course_program(program_id)
        ON DELETE CASCADE
);


CREATE TABLE schedule(
    schedule_id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    group_id INT,
    audience_number INT,
    subject INT,
    date TIMESTAMP DEFAULT NULL,
    FOREIGN KEY(group_id)
        REFERENCES group_student(group_id)
        ON DELETE CASCADE,
    FOREIGN KEY(audience_number)
        REFERENCES audience(audience_number)
        ON DELETE CASCADE,
    FOREIGN KEY(subject)
        REFERENCES course_program(program_id)
        ON DELETE CASCADE
);


CREATE TABLE exercise(
    exercise_id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    title VARCHAR(50) NOT NULL,
    description VARCHAR(255) NOT NULL,
    date_creation TIMESTAMP NOT NULL
    DEFAULT CURRENT_TIMESTAMP,
    program_id INT,
    FOREIGN KEY(program_id)
        REFERENCES course_program(program_id)
        ON DELETE CASCADE
);


CREATE TABLE mark(
    mark_id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    student_id INT,
    exercise_id INT,
    mark INT,
    FOREIGN KEY(student_id)
        REFERENCES student(student_id)
        ON DELETE CASCADE,
    FOREIGN KEY(exercise_id)
        REFERENCES exercise(exercise_id)
        ON DELETE CASCADE
);


CREATE TABLE exam(
    exam_id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    date TIMESTAMP DEFAULT NULL,
    course_id INT,
    FOREIGN KEY(course_id)
        REFERENCES course(course_id)
        ON DELETE CASCADE
);


CREATE TABLE mark_exam(
    mark_exam_id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    student_id INT,
    exam_id INT,
    mark INT NOT NULL,
    FOREIGN KEY(student_id)
        REFERENCES student(student_id)
        ON DELETE CASCADE,
    FOREIGN KEY(exam_id)
        REFERENCES exam(exam_id)
        ON DELETE SET NULL
);
```
### Краткое описание сущностей
1. Student(студент) хранит личные данные студента и указывает на группу к которой он принадлежит.
2. Group(группа) отражает к каким факультетам и отделениям относятся студенты.
3. Faculty type(отделение) хранит возможные отделения и их атрибуты.
4. Faculty(факультет) является связующей для сущностей преподавателей(Teacher), групп(group) и учебных планов(Syllabus).
5. Teacher(преподаватель) связан с факультетом(Faculty) и с конкретным курсом(course) - была использована такая реализация, так как возможна ситуация при которой курс на факультете ведет приглашенный с другого факультета преподаватель.
6. Syllabus(учебный план) является промежуточной сущностью связывающей между собой факультеты, семестры и курсы тем самым формируя сетку учебного плана. Как вариант тут можно  вместо искусственного PK, использовать естественный PK из атрибутов faculty, semester, course.
7. Semester(семестр) хранит список семестров с их атрибутами.
8. Course(Курс) промежуточная сущность для объединения программу курса, экзамена и позиции в учебном плане.
9. Exam(Экзамен) привязан к конкретному курсу.
10. Mark_exam(оценка за экзамен) хранит оценки студентов за экзамены.
11. Course program(программа курса) список дисциплин проводимых в рамках курса, к которым привязывается преподаватель, самостоятельные задания и место в расписании занятий.
12. Program_student(программа студента) - дополнительная сущность описывающая связь many to many между Student и Course_ program. Как вариант тут можно вместо искусственного PK, использовать естественный PK из атрибутов student_program.
13. Exercise(задание для самостоятельной работы) задания в рамках программы курса, которые имеют собственную систему оценивания. Я решил добавить возможность оценивания задания, чисто по логике, так как задание без оценки выглядит странным.
14. Mark(оценка за самостоятельное задание) хранит оценки студентов за задание. Такая иерархия Exercise и Mark выбрана мной из расчёта на то, что задания типовые и одно задание может быть выдано нескольким студентам. В случае если задание является не типовым и выдается персонально каждому студенту, то можно сущности  Exercise и Mark объединить в одну и поставить ей зависимость от сущности Program_student.
15. Schedule(расписание) связывает программу в рамках курса с местом и временем проведения занятия.
16. Audience(аудитория) место проведения занятия, связана с конкретным Зданием. Номер аудитории используется в качестве естественного PK, так как можно рассчитывать на то, что аудитории имеют уникальные номера по всему вузу, если аудитории повторяются по корпусам, то можно использовать составной естественный PK на базе номера аудитории и номера здания. 
17. Building(здание) здесь также использован естественный PK, так как номера зданий точно уникальны, также добавлен атрибут address на случай если нумерация зданий внутри вуза отличается от адреса зданий на карте.

## Часть 2: SQL запросы

### Реализуйте следующие SQL запросы:
Выбрать всех студентов, обучающихся на курсе "Математика".
```js
SELECT s.student_id, s.first_name, s.last_name
FROM student AS s 
JOIN student_program AS sp USING student_id
JOIN course_program AS cp USING program_id
JOIN course AS c USING course_id
WHERE c.name = “Математика”;
```
Обновить оценку студента по курсу.
```js
UPDATE mark_exam AS m
JOIN exam AS ex USING exam_id
JOIN course AS c USING coutse_id
WHERE m.student_id=1 AND c.name=”Математика”; 
```

Выбрать всех преподавателей, которые преподают в здании №3.
```js
SELECT t.teacher_id, t.first_name, t.last_name
FROM teacher AS t
JOIN course_program AS cp USING teacher_id
JOIN schedule AS sch USING program_id
JOIN audience AS a USING audience_number
WHERE a.building=3;
```

Удалить задание для самостоятельной работы, которое было создано более года назад.
```js
DELETE FROM exercise
WHERE YEAR(date)<=DATEADD(YEAR, -1, DATEDIFF(dd, 0, CURRENT_TIMESTAMP));
```

Добавить новый семестр в учебный год.
```js
INSERT INTO semester(start_date, end_date)
VALUE ('2023-09-01 09:00:00', '2023-12-31 09:00:00');
```















1. Разместить код на любом доступном git-резпозитории.
2. Описать файл `README.md`, описать как запустить проект.
3. Соблюдать единый code-style на протяжении всего проекта
4. Обязательна документация для каждого метода, класса и поля. Указание типов обязательно.
5. Первый коммит в проекте должен быть - настройка и конфигурация фреймворка (скелета).
6. Отчет в виде затраченного времени, полнота исполнения задания, а также, возникшие проблемы сложности и их решения, пожелания, комментарий и пр.

## API

- `POST /api/v1/document/` - создаем черновик документа
- `GET /api/v1/document/{id}` - получить документ по id
- `PATCH /api/v1/document/{id}` - редактировать документ
- `POST /api/v1/document/{id}/publish` - опубликовать документ
- `GET /api/v1/document/?page=1&perPage=20` - получить список документов с пагинацией, сортировка в последние созданные сверху.

Дополнительные условия:

- Если документ не найден, то в ответе возвращается 404 код.
- При попытке редактирования документа, который уже опубликован, должно возвращаться 400.
- Попытка опубликовать уже опубликованный документ  возвращает 200.
- Все запросы на конкретный документ возвращают этот документ. [JsonSchema ответа с документом](document-response.json).
- Список документов возвращается в виде массива документов и значений пагинации. [JsonSchema списка документов](document-list-response.json).
- Запрос `PATCH` отправляется с телом json в соответсвующей иерархии документа, все поля, кроме `payload` игнорируются. Если `payload` не передан, то ответ 400.

### Объект документа

```js
document = {
  id: "some-uuid-string",
  status: "draft|published",
  payload: Object,
  createAt: "iso-8601 date time with time zone",
  modifyAt: "iso-8601 date time with time zone"
}
```

[JsonSchema для документа](document.json)

## Патчинг документа

Патчинг проводится согласно [RFC-7396](https://tools.ietf.org/html/rfc7396).
