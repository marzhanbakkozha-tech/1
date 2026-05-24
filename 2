from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import anthropic
import os

app = FastAPI()

# Разрешаем Replit делать запросы к нашему серверу
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

class QueryRequest(BaseModel):
    user_input: str
    business_type: str

@app.post("/ask")
async def ask_claude(request: QueryRequest):
    # Системный промпт с включенным кэшированием Anthropic Prompt Caching
    system_instruction = [
        {
            "type": "text",
            "text": "Ты — высший налоговый и юридический консультант в Казахстане на май 2026 года. Ссылка на старый кодекс запрещена. Распиши ГК РК, ТК РК, Новый НК РК 2026 и КоАП РК (1 МРП = 4325 тенге). Категория бизнеса пользователя: " + request.business_type,
            "cache_control": {"type": "ephemeral"} # ЭТО СНИЖАЕТ СТОИМОСТЬ ПОВТОРНЫХ ЗАПРОСОВ НА 90%
        }
    ]
    
    response = client.messages.create(
        model="claude-3-5-haiku-20241022", # Самая дешевая, точная и быстрая модель
        max_tokens=1500,
        temperature=0.1,
        system=system_instruction,
        messages=[{"role": "user", "content": request.user_input}]
    )
    return {"reply": response.content[0].text}
