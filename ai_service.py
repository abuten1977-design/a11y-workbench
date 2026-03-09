"""
AI Service для A11y Workbench
Использует Gemini API через REST
"""

import requests
import json
import time


class AIService:
    def __init__(self, api_key_file='gemini.env'):
        """Инициализация сервиса"""
        with open(api_key_file, 'r') as f:
            self.api_key = f.read().strip()
        
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        self.model = "gemini-2.5-flash"  # Быстрая модель, 15 req/min
        self.timeout = 30
        
        # Rate limiting: 15 запросов/минуту
        self.max_requests_per_minute = 15
        self.request_times = []  # История запросов
    
    def _check_rate_limit(self):
        """
        Проверить rate limit и подождать если нужно
        Лимит: 15 запросов/минуту
        """
        now = time.time()
        
        # Убрать старые запросы (старше 60 секунд)
        self.request_times = [t for t in self.request_times if now - t < 60]
        
        # Если достигли лимита, подождать
        if len(self.request_times) >= self.max_requests_per_minute:
            oldest = self.request_times[0]
            wait_time = 60 - (now - oldest) + 1  # +1 секунда запас
            
            if wait_time > 0:
                print(f"⏳ Rate limit: ждем {wait_time:.0f}s...")
                time.sleep(wait_time)
                # Очистить после ожидания
                self.request_times = []
        
        # Записать текущий запрос
        self.request_times.append(now)
    
    def generate(self, prompt, temperature=0.7, max_tokens=4000):
        """
        Простая генерация текста
        
        Args:
            prompt: текст запроса
            temperature: креативность (0-2)
            max_tokens: максимум токенов в ответе
        
        Returns:
            str: сгенерированный текст
        """
        url = f"{self.base_url}/models/{self.model}:generateContent"
        
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_tokens
            }
        }
        
        try:
            # Проверить rate limit
            self._check_rate_limit()
            
            response = requests.post(
                url,
                params={"key": self.api_key},
                json=payload,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                text = data["candidates"][0]["content"]["parts"][0]["text"]
                return text
            else:
                raise Exception(f"API error {response.status_code}: {response.text}")
        
        except requests.Timeout:
            raise Exception("API timeout - попробуй еще раз")
        except Exception as e:
            raise Exception(f"API error: {str(e)}")
    
    async def expand_note(self, raw_note, html_code=None, context=None):
        """
        Превратить короткую заметку в структурированный отчет
        
        Args:
            raw_note: короткая заметка ("button unlabeled")
            html_code: HTML код элемента (опционально)
            context: контекст проекта/сессии (опционально)
        
        Returns:
            dict: структурированный отчет
        """
        prompt = self._build_expand_prompt(raw_note, html_code, context)
        
        response_text = self.generate(prompt, temperature=0.5)
        
        # Парсить JSON из ответа
        try:
            # Убрать markdown если есть
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0]
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0]
            
            result = json.loads(response_text.strip())
            return result
        
        except json.JSONDecodeError as e:
            raise Exception(f"Failed to parse AI response: {e}\nResponse: {response_text}")
    
    def _build_expand_prompt(self, raw_note, html_code, context):
        """Построить промпт для expand_note"""
        
        prompt = """You are an accessibility expert assistant for A11y Workbench.

USER PROFILE:
- Blind accessibility specialist, 7 years experience with NVDA
- Tests against WCAG 2.2 Level AA

YOUR TASK:
Transform a short testing note into a professional accessibility defect report.

CRITICAL RULES:
1. NEVER invent screen reader output - use exactly what user reported
2. NEVER invent HTML code - use exactly what was provided
3. Be concise but professional
4. Provide specific, actionable fixes
5. Reference WCAG 2.2 criteria accurately

SEVERITY:
- critical: Blocks task completion
- serious: Major barrier
- moderate: Inconvenience
- minor: Cosmetic

OUTPUT FORMAT (JSON only, no markdown, be concise):
{
  "title": "Clear title (max 80 chars)",
  "steps": ["Step 1", "Step 2", "Step 3"],
  "observed": "What happens (1-2 sentences)",
  "expected": "What should happen (1 sentence)",
  "impact": "User impact (1 sentence)",
  "wcag": [{"id": "4.1.2", "name": "Name, Role, Value", "confidence": 0.95}],
  "severity": "serious",
  "fix": "Code fix (before/after, max 5 lines)",
  "evidence_type": "screen_reader_output"
}

"""
        
        prompt += f"\nUSER NOTE:\n{raw_note}\n"
        
        if html_code:
            prompt += f"\nHTML CODE:\n{html_code}\n"
        
        if context:
            prompt += f"\nCONTEXT:\n"
            if isinstance(context, dict):
                for key, value in context.items():
                    prompt += f"- {key}: {value}\n"
            else:
                prompt += f"{context}\n"
        
        prompt += "\nGenerate the JSON report now:"
        
        return prompt


# Тестовая функция
if __name__ == "__main__":
    print("🧪 Тестирую AI Service...")
    
    ai = AIService()
    
    # Тест 1: Простая генерация
    print("\n1. Простая генерация:")
    result = ai.generate("What is WCAG 4.1.2? Answer in 1 sentence.")
    print(f"✅ {result}")
    
    # Тест 2: Expand note
    print("\n2. Expand note:")
    import asyncio
    
    async def test_expand():
        result = await ai.expand_note(
            raw_note="button unlabeled, NVDA says button only",
            html_code="<button onclick='submit()'>Submit</button>",
            context={"project": "E-commerce", "page": "Checkout"}
        )
        print(f"✅ Title: {result['title']}")
        print(f"✅ WCAG: {result['wcag']}")
        print(f"✅ Severity: {result['severity']}")
    
    asyncio.run(test_expand())
    
    print("\n✅ Все тесты прошли!")
