// Находим элемент с файлом
const fileInput = document.getElementById('avatar')
const form = document.getElementById('form')

function handleSubmit(event) {
  event.preventDefault()

  const formData = new FormData()

  // Добавляем файлы из инпута к данным
  for (let i = 0; i < fileInput.files.length; i++) {
    const file = fileInput.files[i]
    formData.append('avatar', file, file.name)
  }

  // Отправляем файлы на сервер
  fetch('http://localhost:8000/backend/api/upload', {
    method: "POST",
    body: formData,
  })
}

form.addEventListener('submit', handleSubmit)