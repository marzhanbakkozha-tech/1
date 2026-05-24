import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from anthropic import Anthropic

app = FastAPI()

# НАСТРОЙКА CORS: чтобы ваш сайт из Replit мог свободно общаться с Render
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Описываем структуру данных, которую шлет ваш HTML
class LegalQuery(BaseModel):
    user_input: str
    business_type: str

# ПОДКЛЮЧАЕМ КЛЮЧ: теперь Python ищет переменную "APP", как у вас в Render!
anthropic_client = Anthropic(api_key=os.environ.get("APP"))

@app.post("/ask")
async def ask_lawyer(query: LegalQuery):
    try:
        # Системная инструкция для Claude с фокусом на законодательство РК 2026 года
        system_instruction = (
            "Ты — профессиональный налоговый и юридический консультант в Казахстане.\n"
            "Твоя база знаний актуализирована под нормы Налогового кодекса РК "
            "и Предпринимательского кодекса РК на текущий 2026 год.\n"
            f"Категория налогоплательщика, для которой делается расчет: '{query.business_type}'.\n"
            "Отвечай структурированно, ссылайся на статьи кодексов и подбирай размеры штрафов по КоАП "
            f"строго для категории '{query.business_type}'."
        )

        # Запрос к искусственному интеллекту Claude
        message = anthropic_client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2500,
            temperature=0.2,
            system=system_instruction,
            messages=[
                {"role": "user", "content": query.user_input}
            ]
        )
        
        # Возвращаем ответ в поле 'reply', которое ждет ваш index.html в Replit
        return {"reply": message.content[0].text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"status": "Консультант онлайн. Путь /ask готов к обработке POST-запросов."}
