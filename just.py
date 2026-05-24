import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from anthropic import Anthropic

app = FastAPI()

# Разрешаем Replit общаться с Render без блокировок CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LegalQuery(BaseModel):
    user_input: str
    business_type: str

# Проверяем, видит ли вообще сервер ваш ключ в переменной "APP"
api_key_value = os.environ.get("APP")

@app.post("/ask")
async def ask_lawyer(query: LegalQuery):
    # Проверка 1: Если переменная APP вообще пустая в Render
    if not api_key_value:
        return {"reply": "⚠️ Ошибка бэкенда: Переменная окружения 'APP' не найдена в настройках Render!"}
        
    try:
        # Инициализируем клиент внутри запроса для надежности
        anthropic_client = Anthropic(api_key=api_key_value)

        system_instruction = (
            "Ты — профессиональный налоговый и юридический консультант в Казахстане.\n"
            "Твоя база знаний актуализирована под нормы Налогового кодекса РК "
            "и Предпринимательского кодекса РК на текущий 2026 год.\n"
            f"Категория налогоплательщика: '{query.business_type}'.\n"
            "Отвечай структурированно, со ссылками на статьи."
        )

        message = anthropic_client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2500,
            temperature=0.2,
            system=system_instruction,
            messages=[
                {"role": "user", "content": query.user_input}
            ]
        )
        
        return {"reply": message.content[0].text}

    except Exception as e:
        # Если Anthropic вернул ошибку (нет баланса / плохой ключ), мы выведем её текст на сайт!
        return {"reply": f"❌ Ошибка при вызове Claude API: {str(e)}"}

@app.get("/")
def read_root():
    return {"status": "Консультант онлайн."}
