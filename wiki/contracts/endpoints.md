# Контракты конечных точек

Описание: Таблица для хранения информации о языке пользователя.
Название метода

| Название параметра | Тип данных | Описание параметра         | Обязательность | Формат данных |
| ------------------ | ---------- | -------------------------- | -------------- | ------------- |
| id                 | BIGINT     | Идентификатор пользователя | да             | 295           |

-- todo

## POST /validations/validate-up

Валидация учебного плана по заданным критериям.

### Запрос (Request)

```typescript
interface Discipline {
  id: number
  name: string
  credits: number
  examType: string
  hasCourseWork: boolean
  hasPracticalWork: boolean
  department: string
  competenceCodes: string[]
  lectureHours: number
  labHours: number
  practicalHours: number
  sourcePosition?: object
}

interface Row {
  name: string
  color: string
  data: Discipline[][]
}

type Request = Row[]
```

### Ответ (Response)

```typescript
interface ValidationResult {
  message: string
  severity: 'blocking' | 'warning'
  details: Record<string, any>
}

interface Response {
  isValid: boolean
  results: ValidationResult[]
}
```

### Коды ответов

| Код | Описание                  |
| --- | ------------------------- |
| 200 | Успешная валидация        |
| 400 | Ошибка в формате данных   |
| 500 | Внутренняя ошибка сервера |

### Пример ответа

```json
{
  "isValid": false,
  "results": [
    {
      "message": "В семестре 1 количество з.е.: 38 (должно быть 30 ± 6)",
      "severity": "blocking",
      "details": {}
    }
  ]
}
```
