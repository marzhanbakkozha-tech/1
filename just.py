import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from anthropic import Anthropic

app = FastAPI()

# НАСТРОЙКА CORS: чтобы Replit мог без ограничений общаться с Render
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешает запросы со всех сайтов (включая Replit)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Описываем структуру данных, которую отправляет ваш HTML-код
class LegalQuery(BaseModel):
    user_input: str
    business_type: str

# Инициализируем Claude API (Ключ должен лежать в Environment Variables на Render)
anthropic_client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# Этот роут обрабатывает адрес /ask, который прописан в вашем HTML
@app.post("/ask")
async def ask_lawyer(query: LegalQuery):
    try:
        # Формируем умный системный промпт с учетом выбранного бизнеса
        system_instruction = (
            "Ты — высококвалифицированный налоговый и юридический консультант в Казахстане.\n"
            "Твоя база знаний полностью обновлена актуальными нормами Налогового кодекса РК "
            f"и Предпринимательского кодекса РК. Текущий год — 2026.\n"
            f"ВАЖНО: Пользователь определил свою категорию как: '{query.business_type}'.\n"
            "При расчете рисков, проверок или штрафов по КоАП опирайся СТРОГО на санкции, "
            f"предусмотренные именно для категории '{query.business_type}'."
        )

        # Запрос к модели Claude
        message = anthropic_client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2000,
            temperature=0.3,
            system=system_instruction,
            messages=[
                {"role": "user", "content": query.user_input}
            ]
        )
        
        # Возвращаем ответ в поле 'reply', как его ищет ваш index.html
        return {"reply": message.content[0].text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Базовый роут, чтобы при заходе на ссылку в браузере не было ошибки 404
@app.get("/")
def read_root():
    return {"status": "Консультант работает онлайн. Используйте POST /ask"}
