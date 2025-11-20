# Примеры запросов для создания Picture

## Endpoint
```
POST /api/v1/picture/
```

## Параметры запроса

| Параметр | Тип | Обязательный | Описание |
|----------|-----|--------------|----------|
| `title` | String | Да | Заголовок картины |
| `shortDescription` | String | Нет | Краткое описание |
| `description` | String | Нет | Полное описание |
| `image` | MultipartFile | Да | Файл изображения |

---

## 1. Пример с использованием cURL

```bash
curl -X POST http://localhost:8080/api/v1/picture/ \
  -F "title=Моя картина" \
  -F "shortDescription=Краткое описание картины" \
  -F "description=Полное описание картины с деталями" \
  -F "image=@/path/to/image.jpg"
```

### Минимальный запрос (только обязательные поля)

```bash
curl -X POST http://localhost:8080/api/v1/picture/ \
  -F "title=Моя картина" \
  -F "image=@/path/to/image.jpg"
```

---

## 2. Пример с использованием HTTP (raw)

```http
POST /api/v1/picture/ HTTP/1.1
Host: localhost:8080
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW

------WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="title"

Моя картина
------WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="shortDescription"

Краткое описание картины
------WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="description"

Полное описание картины с деталями
------WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="image"; filename="image.jpg"
Content-Type: image/jpeg

[бинарные данные изображения]
------WebKitFormBoundary7MA4YWxkTrZu0gW--
```

---

## 3. Пример с использованием JavaScript (Fetch API)

```javascript
const formData = new FormData();
formData.append('title', 'Моя картина');
formData.append('shortDescription', 'Краткое описание картины');
formData.append('description', 'Полное описание картины с деталями');

// Получаем файл из input
const fileInput = document.querySelector('input[type="file"]');
formData.append('image', fileInput.files[0]);

fetch('http://localhost:8080/api/v1/picture/', {
  method: 'POST',
  body: formData
})
  .then(response => response.json())
  .then(data => {
    console.log('Picture создан:', data);
  })
  .catch(error => {
    console.error('Ошибка:', error);
  });
```

---

## 4. Пример с использованием Axios

```javascript
import axios from 'axios';

const formData = new FormData();
formData.append('title', 'Моя картина');
formData.append('shortDescription', 'Краткое описание картины');
formData.append('description', 'Полное описание картины с деталями');
formData.append('image', fileInput.files[0]);

axios.post('http://localhost:8080/api/v1/picture/', formData, {
  headers: {
    'Content-Type': 'multipart/form-data'
  }
})
  .then(response => {
    console.log('Picture создан:', response.data);
  })
  .catch(error => {
    console.error('Ошибка:', error);
  });
```

---

## 5. Пример с использованием Postman

1. Метод: **POST**
2. URL: `http://localhost:8080/api/v1/picture/`
3. Вкладка **Body** → выберите **form-data**
4. Добавьте следующие поля:

| Key | Type | Value |
|-----|------|-------|
| `title` | Text | Моя картина |
| `shortDescription` | Text | Краткое описание картины |
| `description` | Text | Полное описание картины с деталями |
| `image` | File | [Выберите файл изображения] |

---

## 6. Пример ответа (успешный)

```json
{
  "id": 1,
  "title": "Моя картина",
  "shortDescription": "Краткое описание картины",
  "description": "Полное описание картины с деталями",
  "image": "uploads/1234567890_image.jpg"
}
```

**HTTP Status:** `201 Created`

---

## 7. Примеры ошибок

### Ошибка валидации (пустой заголовок)
**HTTP Status:** `400 Bad Request`

### Ошибка валидации (отсутствует изображение)
**HTTP Status:** `400 Bad Request`

### Ошибка сервера
**HTTP Status:** `500 Internal Server Error`

---

## Примечания

- Все запросы должны использовать `multipart/form-data` для загрузки файла
- Файл изображения будет сохранён в директории `uploads/` с уникальным именем
- Имя файла формируется как: `{timestamp}_{original_filename}`
- Директория `uploads/` будет создана автоматически, если её нет

