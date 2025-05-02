# NeuroNest-AI

NeuroNest-AI هي منصة متقدمة لتنسيق وكلاء الذكاء الاصطناعي تتيح التفاعل السلس مع وكلاء ذكاء اصطناعي متخصصين متعددين. تم تصميم المنصة لتكون معيارية وقابلة للتوسع وآمنة، مع دعم الوصول من أجهزة متعددة والتشغيل دون اتصال بالإنترنت.

## الميزات الرئيسية

- **وكلاء ذكاء اصطناعي متعددين**: التفاعل مع وكلاء متخصصين مثل Thinker و Developer والمزيد
- **تنسيق الوكلاء**: توجيه ذكي للطلبات إلى الوكيل الأنسب
- **ذاكرة المحادثة**: تخزين دائم للمحادثات مع وعي بالسياق
- **دعم الأجهزة المتعددة**: الوصول إلى محادثاتك من أي جهاز
- **مصادقة آمنة**: مصادقة قائمة على JWT مع إدارة الأجهزة
- **واجهة أمامية حديثة**: واجهة مستخدم متجاوبة مبنية باستخدام Next.js و Tailwind CSS
- **خلفية قابلة للتوسع**: خلفية FastAPI مع PostgreSQL و Redis
- **نشر مُحاوَى**: نشر سهل باستخدام Docker و Docker Compose

## البنية

يتبع المشروع بنية معيارية حديثة:

```
NeuroNest-AI/
│
├── agents/                   # تنفيذات وكلاء الذكاء الاصطناعي
│   ├── base_agent.py         # فئة الوكيل الأساسية
│   ├── thinker_agent.py      # وكيل التفكير التحليلي
│   ├── developer_agent.py    # وكيل البرمجة والمشاكل التقنية
│   ├── autogen_agent.py      # إطار عمل AutoGen متعدد الوكلاء
│   └── crewai_agent.py       # إطار عمل وكيل CrewAI
│
├── api/                      # مسارات ونقاط نهاية FastAPI
│   └── routes/
│       ├── auth.py           # نقاط نهاية المصادقة
│       ├── chat.py           # نقاط نهاية المحادثة والرسائل
│       └── agents.py         # نقاط نهاية إدارة الوكلاء
│
├── core/                     # مكونات النظام الأساسية
│   ├── orchestrator.py       # منطق تنسيق الوكلاء
│   ├── memory.py             # إدارة ذاكرة المحادثة
│   └── security.py           # أدوات الأمان
│
├── database/                 # نماذج قاعدة البيانات وأدواتها
│   ├── base.py               # إعداد SQLAlchemy الأساسي
│   ├── models.py             # نماذج قاعدة البيانات
│   └── session.py            # إدارة جلسة قاعدة البيانات
│
├── frontend/                 # تطبيق Next.js للواجهة الأمامية
│
├── config/                   # إدارة الإعدادات
│   └── settings.py           # إعدادات التطبيق
│
├── alembic/                  # أدوات هجرة قاعدة البيانات
│
├── docker-compose.yml        # تكوين Docker Compose
├── Dockerfile                # تكوين Docker للخلفية
└── pyproject.toml            # إدارة الحزم باستخدام Poetry
```

## البدء

### المتطلبات الأساسية

- Python 3.10 أو أعلى
- Node.js 18 أو أعلى
- Docker و Docker Compose (للنشر المُحاوَى)
- PostgreSQL (للتطوير المحلي)
- Redis (للتطوير المحلي)

### التثبيت

1. استنساخ المستودع:

```bash
git clone https://github.com/yourusername/NeuroNest-AI.git
cd NeuroNest-AI
```

2. إعداد الخلفية:

```bash
# تثبيت Poetry
pip install poetry

# تثبيت الاعتماديات
poetry install

# إنشاء ملف .env
cp .env.example .env
# تعديل ملف .env بإعداداتك

# تشغيل هجرات قاعدة البيانات
poetry run alembic upgrade head

# تشغيل خادم الخلفية
poetry run uvicorn main:app --reload
```

3. إعداد الواجهة الأمامية:

```bash
cd frontend
npm install
npm run dev
```

### النشر باستخدام Docker

لنشر المجموعة الكاملة باستخدام Docker:

```bash
# إنشاء ملف .env
cp .env.example .env
# تعديل ملف .env بإعداداتك

# بناء وتشغيل الحاويات
docker-compose up -d
```

## توثيق API

بمجرد تشغيل الخادم، يمكنك الوصول إلى توثيق API على:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## المساهمة

المساهمات مرحب بها! يرجى عدم التردد في تقديم طلب سحب.

## الترخيص

هذا المشروع مرخص بموجب ترخيص MIT - راجع ملف LICENSE للحصول على التفاصيل.