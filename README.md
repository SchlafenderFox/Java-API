# API

### Installation
  - Install `git bash`.
  - Install `docker` and `docker-compose`.
  - Clone repository:
    - ```git clone https://github.com/SchlafenderFox/Java-API.git```
  - Enter to repository folder.
  - Open `terminal (Linux)` or `cmd (Windows)`.
  - Run API:
    - ```docker-compose up -d --build```
  - Ready.

### Info
  - Application port: `9999`
  - Run command:
    - ```docker-compose up -d --build```
  - Default request address:
    - ```localhost:9999/api/get-news/```  
  
### Category:
 - Allow category:
 - ```
   "Всі",
   "Економіка",
   "За кордоном",
   "Здоров'я",
   "Київські новини",
   "Курйози",
   "Події",
   "Політика України",
   "Спорт",
   "Суспільство",
   "Технології",
   "Фоторепортаж",
   "Шоу-бізнес"
   ``` 

### Language:
 - Allow language:
 - ```
   "ua",
   "ru",
   "en"
   ``` 


### Main endpoints:
   
  - `/api/get-news/`:
    - method `POST`
    - returns `news`
    - parameters:
      - `category`:
        - type: `string`
        - required: `True`
        - default: `Всі`
        - example: `Економіка`
      - `time`:
        - type: `string`
        - required: `False`
        - defaults: `00:00-23:59`
        - example: `hh:mm`, `hh:mm-hh:mm`, `09:00-10:00`
      - `date`:
        - type: `string`
        - required: `False`
        - defaults: `today`
        - example: `dd.mm.yyyy`, `dd.mm.yyyy-dd.mm.yyyy`, `01.01.2019-01.12.2019`
      - `language`:
        - type: `string`
        - required: `False`
        - defaults: `ua`
        - example: `en`
      
      - response format:
        ```json
          {
                "status": "ok",
                "result": [],
                "error": ""
          }
           
        ```
        ```json
          {
            "status": "error",
            "result": [],
            "error": "error message"
          }
        ```
      - response example:
        ```json
        {
          "status": "ok",
          "result": [
                      {
                       "title": "Трамп у розмові з Мей оскаржував висновки розвідслужб Великої Британії щодопричетності Росії до отруєння Скрипаля, - WP",
                       "date": "05.10.19",
                       "time": "23:47",
                       "text": "Президент Сполучених Штатів Америки Дональд Трамп у телефонній розмові з колишнім прем'єр-міністром Великої Британії Терезою Мей засумнівався впричетності Росії до отруєння Скрипалів.", 
                       "url": "https://censor.net.ua/ua/news/3152326/tramp_u_rozmovi_z_meyi_oskarjuvav_vysnovky_rozvidslujb_velykoyi_brytaniyi_schodo_prychetnosti_rosiyi",
                       "img-url": "https://storage1.censor.net/images/1/1/b/b/11bb19b9be3de92f26e09d8b37ec3d8c/censor_news_small.jpg"
                      }
                    ],
          "count": 1,
          "error": ""
        }
        ```
