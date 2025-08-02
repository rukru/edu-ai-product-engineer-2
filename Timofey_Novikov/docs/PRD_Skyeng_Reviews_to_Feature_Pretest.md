# PRD — From User Reviews to Feature Pre‑Test (HW#2) — Enhanced v2.0

**Проект:** Skyeng — высокоскоростной анализ отзывов → персоны → углубленный виртуальный прётест фич  
**Цель:** Построить end‑to‑end пайплайн с оптимизированной скоростью, который
1) **быстро собирает** отзывы из App Store (параллельная обработка, кеширование),
2) **ускоренно извлекает** инсайты и запросы на фичи (пайплайн оптимизации),
3) генерирует 3–5 персон на основе отзывов (с учётом портретов клиента),
4) проводит **углубленный виртуальный «совет пользователей»** с follow-up вопросами как в качественном исследовании,
5) сохраняет полный лог интервью с детальной аналитикой в `.txt`.

**Enhanced KR:**
- ≥10k отзывов собраны и нормализованы **за <2 часа** (vs стандартные 8-12 часов).
- ≥80% отзывов классифицированы по типам **за <30 минут** обработки.
- ≥5 устойчивых тем feature-запросов с **приоритизацией по impact**.
- 3–5 персон с верифицированными цитатами + **глубинные интервью 15+ вопросов**.
- 2–3 фичи прошли **углубленный прётест** (3 раунда + follow-up), сгенерированы детальные отчеты.
- **Качественная методология**: каждая персона отвечает на 5-7 уточняющих вопросов по каждой фиче.

---

## 1. Скоуп

**Включено**
- Сбор отзывов App Store (RU + доп. страны).
- Нормализация, фильтрация по языку, перевод при необходимости.
- Topic mining и извлечение запросов на фичи.
- Генерация персон и их уточнение на базе предоставленных портретов.
- Виртуальный совет пользователей (мультиагентная симуляция).
- Экспорты логов и отчётов в `.txt`.

**Исключено**
- Реальные интервью и UI-дашборд (кроме CLI/ноутбуков).
- Ручная модерация токсичности.

---

## 2. Высокоскоростные источники данных: App Store (Skyeng)

**Параллельный сбор (5x ускорение):**
- **Мультипоточность**: 8-16 воркеров для параллельного сбора по странам/периодам.
- **Hybrid источники**: `app-store-scraper` + RSS iTunes + AppFollow API (резервирование).
- **Smart pagination**: динамическое определение оптимального размера страниц.
- **Поля расширенные**: `review_id, app_id, author, rating, title, text, lang, version, country, date, helpful_count, total_votes`.
- **Агрессивное кеширование**: Redis/местный кеш для избежания повторных запросов.
- **Rate limiting optimization**: адаптивные задержки на основе response time.

**Ускоренная нормализация (10x speedup):**
- **Batch processing**: обработка пакетами по 1000 отзывов параллельно.
- **Быстрый детект языка**: `fastText lid.176` с предварительной фильтрацией по символам.
- **Conditional translation**: перевод только non-RU отзывов >50 символов.
- **Vectorized cleaning**: pandas/numpy операции вместо циклов.
- **Pipeline optimization**: streaming обработка без промежуточных файлов.

**Performance targets:**
- **Сбор**: 10k отзывов за <2 часа (vs 8-12 часов стандартно)
- **Нормализация**: <30 минут для полного dataset
- **Memory efficiency**: <2GB RAM для обработки 50k отзывов

---

## 3. Оптимизированные модели и обработка (RU) — Speed-First Pipeline

**Ускоренные эмбеддинги (3x faster):**
- **Primary**: `all-MiniLM-L6-v2` (быстрая, 22MB) для первичной обработки
- **Secondary**: `paraphrase-multilingual-MiniLM-L12-v2` только для спорных случаев
- **Batch encoding**: обработка пакетами по 512 текстов
- **GPU acceleration**: CUDA если доступно, fallback на CPU optimized

**Параллельная кластеризация:**
- **Fast BERTopic**: UMAP с n_neighbors=5, min_dist=0.0 для скорости
- **HDBSCAN optimized**: min_cluster_size=10, algorithm='boruvka_kdtree'
- **Hierarchical merging**: автоматическое слияние похожих кластеров (cosine >0.85)

**Ускоренное извлечение фич (Feature Mining Pipeline):**
- **Pattern matching first**: regex для "хочу/нужно/добавьте/не хватает/missing" (90% покрытие за секунды)
- **KeyBERT selective**: применяется только к оставшимся 10% сложных случаев
- **Feature template matching**: предобученные шаблоны для EdTech domain
- **Impact scoring**: автоматический расчет приоритета (частота × sentiment × rating impact)

**Smart классификация (Hybrid Approach):**
- **Rule-based pre-filter**: быстрая классификация 70% очевидных случаев
- **LLM for ambiguous**: GPT-4 только для неоднозначных отзывов
- **Batch inference**: группировка похожих отзывов для LLM обработки
- **Классы расширенные**: `feature_request, bug_report, usability, pricing, praise, performance, content_quality, other`

**Real-time приоритизация фич:**
- **Urgency signals**: spike detection в негативных отзывах
- **Business impact**: интеграция с метриками retention/conversion
- **Effort estimation**: автоматическая оценка сложности разработки
- **ROI scoring**: потенциальный impact vs estimated effort

**Performance benchmarks:**
- **Feature extraction**: 10k отзывов за <15 минут
- **Кластеризация**: <5 минут для 50k отзывов  
- **Классификация**: <10 минут для полного dataset
- **End-to-end**: от сырых отзывов до приоритизированных фич за <45 минут

---

## 4. Мультиагентная архитектура и оркестратор

**Фреймворк (предложение):** LangGraph (возможна замена на CrewAI/OpenAI Agents SDK).

**Агенты (расширенные с качественной методологией):**
1. **CollectorAgent** — параллельный сбор отзывов → `reviews.parquet`.
2. **PreprocessorAgent** — ускоренная очистка/язык → `reviews_clean.parquet`.
3. **InsightMinerAgent** — быстрые эмбеддинги, BERTopic, KeyBERT → `insights.jsonl`.
4. **FeatureFormulatorAgent** — 2–3 приоритизированные фичи → `features.json`.
5. **PersonaBuilderAgent** — 3–5 детализированных персон → `personas.json`.
6. **BoardModeratorAgent** — углубленный сценарий с follow-up логикой.
7. **PersonaSpeakerAgents [N]** — участники с памятью и адаптивными ответами.
8. **QualitativeInterviewerAgent** — **NEW**: специалист по follow-up вопросам.
9. **ConversationAnalyzerAgent** — **NEW**: анализ динамики диалога.
10. **AnalystAgent** — углубленная сводка с качественными инсайтами.
11. **LoggerAgent** — детализированное протоколирование → `detailed_interview_log.txt`.
12. **Orchestrator (LangGraph)** — управление адаптивными интервью.

**Граф стадий (Enhanced):**  
`Collector → Preprocessor → InsightMiner → (FeatureFormulator, PersonaBuilder) → BoardModerator ↔ (PersonaSpeakers ↔ QualitativeInterviewer) → ConversationAnalyzer → Analyst → Logger`

---

## 4.1. NEW: Углубленная качественная методология — Follow-up Interview System

### Архитектура адаптивных интервью

**QualitativeInterviewerAgent** — центральный агент для проведения глубинных интервью:

**Роли и функции:**
- **Probe specialist**: генерирует уточняющие вопросы на основе ответов персон
- **Context keeper**: отслеживает контекст разговора для связных follow-up
- **Insight detector**: определяет моменты для углубления в детали
- **Interview flow manager**: управляет естественным ходом беседы

### Типы follow-up вопросов (по UX Research methodology)

#### 1. **Clarification Probes** (Уточняющие)
```
Persona ответила: "Мне не нравится, что приложение тормозит"
Follow-up: "Можете конкретнее описать, в какие моменты вы замечаете торможение? Это происходит при открытии урока, во время просмотра видео, или в другие моменты?"
```

#### 2. **Emotional Probes** (Эмоциональные)
```
Persona: "Было бы удобно иметь офлайн режим"
Follow-up: "Что вы чувствуете, когда понимаете, что не можете заниматься без интернета? Расскажите о ситуации, когда это вас особенно расстроило."
```

#### 3. **Behavioral Probes** (Поведенческие)
```
Persona: "Хотелось бы больше практики"
Follow-up: "Покажите, как обычно проходит ваш урок сейчас. Что именно вы делаете после изучения теории? Сколько времени уделяете практике?"
```

#### 4. **Comparative Probes** (Сравнительные)
```
Persona: "В других приложениях удобнее"
Follow-up: "Какие именно приложения вы имеете в виду? Что конкретно в них работает лучше? Можете привести пример?"
```

#### 5. **Hypothetical Probes** (Гипотетические)
```
Persona: "Нужны напоминания"
Follow-up: "Представьте, что у вас есть идеальная система напоминаний. Как она должна работать? В какое время дня? Какие слова должны быть в уведомлении?"
```

#### 6. **Constraint Probes** (Барьеры/Ограничения)
```
Persona: "Было бы классно"
Follow-up: "Что могло бы помешать вам использовать эту функцию? Какие есть опасения? За что вы бы не хотели платить дополнительно?"
```

### Структура углубленного интервью по каждой фиче

#### **Phase 1: Initial Reaction** (3-5 минут)
- Первая реакция на концепцию фичи
- Спонтанные ассоциации и эмоции
- Понимание ценности

#### **Phase 2: Deep Exploration** (8-12 минут)
**Systematic follow-up по категориям:**

1. **Контекст использования:**
   - "В какой ситуации вы бы использовали это?"
   - "Как часто возникает такая потребность?"
   - "Что происходит сейчас, когда вы сталкиваетесь с этой проблемой?"

2. **Детали взаимодействия:**
   - "Как именно вы видите работу с этой функцией?"
   - "Какие шаги вы бы предприняли?"
   - "Что должно происходить дальше?"

3. **Эмоциональная сторона:**
   - "Что вы чувствуете, когда думаете об этой возможности?"
   - "Какие опасения у вас есть?"
   - "Что вас больше всего радует в этой идее?"

4. **Барьеры и ограничения:**
   - "Что могло бы помешать вам это использовать?"
   - "При каких условиях эта функция была бы бесполезной?"
   - "Какая цена была бы слишком высокой?"

5. **Сравнения и альтернативы:**
   - "Как вы решаете эту проблему сейчас?"
   - "Видели ли вы что-то похожее в других приложениях?"
   - "Что работает лучше/хуже?"

#### **Phase 3: Co-creation** (3-5 минут)
- "Как бы вы улучшили эту идею?"
- "Что бы вы добавили или убрали?"
- "Какой была бы идеальная версия?"

### Алгоритм генерации follow-up вопросов

```python
class QualitativeInterviewerAgent:
    def generate_followup(self, persona_response, context):
        # 1. Анализ ответа персоны
        response_analysis = {
            'sentiment': self.analyze_sentiment(persona_response),
            'specificity': self.measure_specificity(persona_response),
            'emotional_indicators': self.detect_emotions(persona_response),
            'knowledge_gaps': self.identify_gaps(persona_response, context)
        }
        
        # 2. Выбор типа follow-up на основе анализа
        if response_analysis['specificity'] < 0.3:
            question_type = 'clarification'
        elif response_analysis['emotional_indicators']:
            question_type = 'emotional'
        elif 'comparison' in persona_response.lower():
            question_type = 'comparative'
        else:
            question_type = 'behavioral'
            
        # 3. Генерация персонализированного вопроса
        return self.craft_question(question_type, persona_response, context)
```

### Пример углубленного интервью

**Фича**: "Адаптивные напоминания на основе прогресса"

```
[10:05] Moderator: Мария, как вы относитесь к идее напоминаний, которые адаптируются под ваш прогресс?

[10:06] Persona_Maria (Мама школьника): Звучит интересно! У нас всегда проблема с регулярностью занятий.

[10:06] QualitativeInterviewer: Можете конкретнее рассказать о проблеме с регулярностью? Что происходит сейчас, когда ребенок пропускает занятия?

[10:07] Persona_Maria: Ну, сын забывает заниматься, я забываю напомнить... А потом оказывается, что мы отстали от программы.

[10:07] QualitativeInterviewer: Что вы чувствуете в момент, когда понимаете, что отстали? И как это влияет на мотивацию ребенка?

[10:08] Persona_Maria: Расстраиваюсь, честно говоря. А сын начинает нервничать, что много пропустил...

[10:08] QualitativeInterviewer: Представьте идеальную систему напоминаний для вашей семьи. Как она должна работать? Кому и когда приходят уведомления?

[10:09] Persona_Maria: Наверное, мне на телефон должно приходить, что пора заниматься. Но не навязчиво... И чтобы показывало, что именно сегодня нужно изучить.

[10:09] QualitativeInterviewer: "Не навязчиво" - это важная деталь. Что для вас означает навязчивость в уведомлениях? Приведите пример плохого уведомления.

[10:10] Persona_Maria: Когда каждые полчаса пишет "Время заниматься!". Это раздражает. Лучше один раз, но с понятным объяснением, зачем это важно именно сейчас.
```

### Адаптивная логика углубления

**Triggers для follow-up:**
- **Неопределенные ответы** → Clarification probes
- **Эмоциональные слова** → Emotional probes  
- **Упоминание других продуктов** → Comparative probes
- **Краткие ответы** → Behavioral probes
- **Противоречия** → Constraint probes

**Глубина интервью:**
- **Level 1**: Поверхностный ответ → 1-2 follow-up
- **Level 2**: Детализированный ответ → 3-4 follow-up  
- **Level 3**: Противоречивый/интересный ответ → 5-7 follow-up

---

## 5. Расширенные схемы данных

**`reviews.parquet`** — `review_id, created_at, rating, text, lang, version, country, helpful_count, total_votes`  
**`insights.jsonl`** — `cluster_id, label, top_keywords, sample_reviews[], support, sentiment, type, impact_score, urgency_level`  
**`features.json`** — `feature_id, name, problem, JTBD, hypothesis, success_metrics, risks, priority_score, effort_estimate, roi_score`  
**`personas.json`** — `persona_id, name, age_range, role, goals, pains, tech_level, quotes[], evidence_clusters[], constraints_from_client[], personality_traits, communication_style`  

**NEW Enhanced Outputs:**
**`detailed_interview_log.txt`** — углубленный стенограф с follow-up вопросами и анализом  
**`conversation_analysis.json`** — анализ динамики диалога, паттернов ответов, эмоциональных триггеров  
**`feature_reports_enhanced.txt`** — отчёт с качественными инсайтами из углубленных интервью  
**`persona_insights.json`** — детальные поведенческие паттерны и мотивации персон  
**`followup_effectiveness.json`** — метрики эффективности уточняющих вопросов

---

## 6. Расширенные промпты (RU) — с качественной методологией

**Классификация отзыва (с приоритизацией):**
```text
Задача: отнеси отзыв к одному из классов: 
[feature_request, bug_report, usability, pricing, praise, performance, content_quality, other]. 
Дополнительно оцени impact_score (1-10) и urgency_level (low/medium/high).
Ответ дай в JSON: {"class": "...", "rationale": "...", "impact_score": X, "urgency_level": "..."}
Отзыв: "{текст}"
```

**Ускоренная формулировка фичи:**
```text
Ввод: тема (keywords, цитаты, частота), примеры отзывов.
Выведи JSON с быстрой оценкой приоритета:
{name, problem, JTBD, hypothesis, success_metrics, risks, priority_score, effort_estimate, roi_score}
priority_score = impact × urgency / effort_estimate
```

**NEW: QualitativeInterviewer System Prompt:**
```text
Ты — профессиональный UX-исследователь, специалист по качественным интервью. 
Твоя задача — задавать уточняющие вопросы персонам, чтобы получить глубокие инсайты.

Правила ведения интервью:
1. Анализируй каждый ответ персоны на предмет специфичности, эмоций, противоречий
2. Выбирай тип follow-up: clarification/emotional/behavioral/comparative/hypothetical/constraint
3. Задавай max 2 уточняющих вопроса подряд, затем дай персоне развить мысль
4. Используй активное слушание: "Правильно ли я понимаю, что...", "Получается..."
5. Ищи конкретные примеры: "Можете привести пример?", "Расскажите о последнем случае"
6. Исследуй эмоции: "Что вы чувствуете, когда...", "Какие эмоции вызывает..."

Context: {current_feature}, {persona_profile}, {conversation_history}
Ответ персоны: {persona_response}
Твой follow-up:
```

**NEW: Enhanced Persona Speaker Prompt:**
```text
Ты — {PersonaName}. 
Базовый профиль: {goals}, {pains}, {tech_level}
Личностные черты: {personality_traits}
Стиль общения: {communication_style}
Evidence из отзывов: {evidence_clusters}

Важные принципы поведения:
1. Отвечай исходя из своего опыта и контекста жизни
2. Используй конкретные примеры из своей "жизни" 
3. Проявляй эмоции соответственно ситуации
4. Иногда сомневайся, задавай встречные вопросы
5. Помни предыдущие вопросы в разговоре - сохраняй согласованность
6. Не соглашайся со всем подряд - имей свое мнение

Текущая фича для обсуждения: {current_feature}
История разговора: {conversation_history}
Вопрос/тема: {current_question}
Твой ответ (от лица персоны):
```

**NEW: Conversation Analyzer Prompt:**
```text
Проанализируй диалог между QualitativeInterviewer и персонами.
Выяви:
1. Эффективность уточняющих вопросов (какие дали больше инсайтов)
2. Эмоциональную динамику разговора
3. Ключевые insight моменты
4. Паттерны в ответах персон
5. Области, требующие дополнительного исследования

Формат ответа:
{
  "effective_questions": [...],
  "emotional_journey": {...},
  "key_insights": [...],
  "response_patterns": {...},
  "research_gaps": [...]
}

Диалог: {conversation_log}
```

**Enhanced Модерация борда:**
```text
Цель — углубленный прётест фичи "{name}". 
Структура: 3 основных раунда + follow-up раунд.

Round 1: Initial Reactions (5 мин)
Round 2: Deep Exploration с QualitativeInterviewer (15 мин)  
Round 3: Co-creation и барьеры (8 мин)
Follow-up Round: Уточнения по противоречиям (5 мин)

Ты модерируешь, но QualitativeInterviewer ведет углубленные вопросы.
Твоя роль: направляй обсуждение, выявляй противоречия, подводи итоги раундов.
```

**Enhanced Аналитик (итог):**
```text
Суммируй результаты углубленного прётеста фичи "{name}":

1. Executive Summary (краткий вывод)
2. Qualitative Insights (из follow-up интервью)
3. Emotional Journey Map (как персоны реагировали)
4. Key Barriers и их критичность  
5. Unexpected Findings (неожиданные открытия)
6. Implementation Recommendations с приоритизацией
7. Open Questions для дальнейшего исследования
8. Success Criteria (как измерить успех фичи)

Используй цитаты персон для подтверждения выводов.
```

---

## 7. Выводы/артефакты

- `data/reviews.parquet`
- `out/insights.jsonl`
- `out/features.json`
- `out/personas.json`
- `out/virtual_board_log.txt`
- `out/feature_reports.txt`

**Пример `virtual_board_log.txt`:**
```text
[2025-08-01 10:05] Moderator: Фича "Умные напоминания..."
[10:06] Persona_A (Мама школьника): ...
[10:07] Persona_B (Студент вуза): ...
--- Round 2: сценарии ---
--- Round 3: барьеры и улучшения ---
```

---

## 8. Расширенные критерии приёмки

**Speed & Performance:**
- Сбор 10k отзывов за <2 часа (vs стандартные 8-12 часов)
- Обработка и feature extraction за <45 минут end-to-end
- Идемпотентный сбор, инкрементальные догрузки, детальные логи

**Quality & Depth:**
- От «сырых отзывов» до приоритизированных `features.json` и детализированных `personas.json` — одной командой
- Виртуальный совет: ≥4 раунда (включая follow-up), участники опираются на данные
- **NEW**: Каждая персона отвечает на ≥5 уточняющих вопросов по каждой фиче
- **NEW**: QualitativeInterviewer генерирует адаптивные follow-up вопросы

**Enhanced Outputs:**
- Генерация 5 типов отчетов: стандартный лог + углубленный интервью + анализ диалога + инсайты персон + метрики эффективности
- **Conversation quality**: ≥70% follow-up вопросов должны приводить к новым инсайтам
- **Persona consistency**: персоны должны сохранять согласованность в ответах на протяжении интервью

---

## 9. Стек, репозиторий и запуск

**Enhanced Стек:** Python 3.10+, LangGraph (или CrewAI/OpenAI Agents SDK), pandas/pyarrow, sentence-transformers, umap-learn, hdbscan, bertopic, keybert, fasttext, pydantic, redis (кеширование), concurrent.futures (параллелизация), (опц.) argostranslate.  

**Структура репо:**
```
.
├─ data/
├─ out/
├─ src/
│  ├─ collectors/
│  │  ├─ appstore_parallel.py      # Параллельный сбор
│  │  └─ cache_manager.py         # Redis кеширование
│  ├─ preprocess/
│  │  ├─ fast_clean.py           # Ускоренная очистка
│  │  └─ batch_processor.py      # Batch обработка
│  ├─ insights/
│  │  ├─ speed_topic_modeling.py # Оптимизированная кластеризация
│  │  ├─ hybrid_feature_extraction.py # Rule-based + LLM
│  │  └─ priority_scoring.py     # Автоматическая приоритизация
│  ├─ personas/
│  │  ├─ enhanced_persona_builder.py # Детализированные персоны
│  │  └─ personality_traits.py   # Черты характера
│  ├─ agents/
│  │  ├─ moderator_enhanced.py   # Улучшенная модерация
│  │  ├─ persona_speaker_v2.py   # Персоны с памятью
│  │  ├─ qualitative_interviewer.py # NEW: Follow-up специалист
│  │  ├─ conversation_analyzer.py # NEW: Анализ диалогов
│  │  └─ analyst_enhanced.py     # Углубленная аналитика
│  ├─ orchestration/
│  │  ├─ langgraph_enhanced.py   # Адаптивный граф
│  │  └─ interview_flow_manager.py # Управление интервью
│  └─ io/
│     ├─ enhanced_logger.py      # Детальное логирование
│     └─ report_generator.py     # Множественные отчеты
├─ notebooks/eda.ipynb
├─ configs/
│  ├─ personas_seed.yaml
│  └─ prompts.yaml
├─ run_pipeline.py
└─ README.md
```

**Псевдокод `run_pipeline.py`:**
```python
def main():
    raw = CollectorAgent().run(app_id=SKYENG_APP_ID, countries=['RU','KZ','UA','BY','TR'])
    clean = PreprocessorAgent().run(raw)
    insights = InsightMinerAgent().run(clean)
    features = FeatureFormulatorAgent().run(insights, k=3)
    personas = PersonaBuilderAgent().run(clean, seed_personas="configs/personas_seed.yaml", n=5)
    log_path = BoardModeratorAgent().run(features, personas)
    reports = AnalystAgent().run(log_path, features)
    LoggerAgent().export(log_path, reports)
```

---

## 10. Риски и меры

- **Сбор App Store:** лимиты/блокировки → троттлинг, кеш, резервные источники.
- **Качество тем:** шумы в кластеризации → пороги частоты, LLM‑нормализация, ручная ревизия top-N.
- **Синтетические интервью:** риск конформности → конфликтные вопросы модератора, жёсткий контекст персоны.
- **Русский язык:** проверка на подвыборке, корректные RU‑модели.

---

## 11. Что нужно от заказчика

1) App Store **App ID для Skyeng** и список стран/языков.  
2) **Портреты клиентов** (seed) — поля и ограничения.  
3) Выбор фреймворка: **LangGraph / CrewAI / OpenAI Agents SDK**.  
4) Подтверждение путей экспорта (`out/*.txt`, JSON).
5) **NEW**: Бюджет на LLM API calls для углубленных интервью.
6) **NEW**: Требования к глубине качественного исследования (5-7 вопросов vs 15+ вопросов).

---

## 12. NEW: Ключевые улучшения v2.0

### 🚀 **Speed Optimization (5-10x ускорение)**
- **Параллельный сбор**: 8-16 воркеров для одновременного сбора из разных источников
- **Smart preprocessing**: rule-based фильтрация 70% очевидных случаев перед LLM
- **Batch processing**: векторизованные операции pandas/numpy
- **Aggressive caching**: Redis для избежания повторных API calls
- **Timeline**: 10k отзывов за <2 часа vs стандартные 8-12 часов

### 🎭 **Qualitative Research Methodology**
- **QualitativeInterviewerAgent**: специализированный агент для follow-up вопросов
- **6 типов уточнений**: clarification, emotional, behavioral, comparative, hypothetical, constraint
- **Adaptive questioning**: до 7 уточняющих вопросов на основе анализа ответов персон
- **Conversation memory**: персоны помнят контекст и сохраняют согласованность
- **Real-time analysis**: ConversationAnalyzerAgent анализирует динамику диалога

### 📊 **Enhanced Intelligence**
- **Impact scoring**: автоматическая приоритизация фич по формуле (impact × urgency / effort)
- **Emotion tracking**: отслеживание эмоциональной динамики в интервью
- **Pattern recognition**: выявление поведенческих паттернов персон
- **Insight depth**: 5 типов отчетов vs стандартные 2

### 🎯 **Business Value**
- **Time to insights**: от 12+ часов до <3 часов end-to-end
- **Research depth**: от поверхностных ответов к глубинным инсайтам как в реальном UX research
- **Actionable outputs**: приоритизированные фичи с ROI оценками
- **Scalability**: возможность обработки 50k+ отзывов без потери качества

**ROI**: 4-5x ускорение + качественные инсайты на уровне профессионального UX research = значительная экономия времени продуктовой команды при повышении качества принимаемых решений.
