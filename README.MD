# README

## Brief

Небольшое тестовое для компании ZiMAD.

## Notes

Сначала пробовал читать пдф через pypdf2, но, вероятно, это слишком низкоуровневая либа. Просто так оттуда текст с
местоположением не вытащить. В итоге использовал `fitz`. Картинки все равно вытащить не могу: не находить их
href'ы. Так их можно было вытащить и прям в base64 хранить (как делают в вебе).