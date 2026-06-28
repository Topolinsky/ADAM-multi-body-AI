import socket
import json
import os
import re
from datetime import datetime

# ===== НАСТРОЙКИ =====
HOST = "127.0.0.1"
PORT = 1234
AI_FOLDER = r"C:\AI"
MEMORY_FILE = os.path.join(AI_FOLDER, "memory.txt")
HISTORY_FILE = os.path.join(AI_FOLDER, "history.txt")
MEMORY_LIMIT = 15000

def ensure_folder():
    if not os.path.exists(AI_FOLDER):
        os.makedirs(AI_FOLDER)
    for f in [MEMORY_FILE, HISTORY_FILE]:
        if not os.path.exists(f):
            open(f, 'w', encoding='utf-8').close()

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            return f.read().strip()
    return ""

def load_full_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
            return f.read()
    return ""

def save_dialog(user_msg, ai_msg, is_start=False, is_exit=False):
    with open(MEMORY_FILE, 'a', encoding='utf-8') as f:
        if is_start:
            f.write(f"\n[СЕССИЯ НАЧАЛАСЬ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]\n")
        elif is_exit:
            f.write(f"[СЕССИЯ ЗАВЕРШЕНА: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]\n")
        else:
            f.write(f"User: {user_msg}\nAI: {ai_msg}\n")

def print_logo():
    print(r"""
    ╔══════════════════════════════════════════════════════════════════╗
    ║            █████╗ ██████╗  █████╗ ███╗   ███╗                    ║
    ║           ██╔══██╗██╔══██╗██╔══██╗████╗ ████║                    ║
    ║           ███████║██║  ██║███████║██╔████╔██║                    ║
    ║           ██╔══██║██║  ██║██╔══██║██║╚██╔╝██║                    ║
    ║           ██║  ██║██████╔╝██║  ██║██║ ╚═╝ ██║                    ║
    ║           ╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝                    ║
    ║                      ╔═════════════════╗                         ║
    ║                      ║     = ADAM =    ║                         ║
    ║                      ╚═════════════════╝                         ║
    ║                         Multi-Body-AI    ver 1.33                ║
    ║                     +   memory body (allready)                   ║
    ║                     -   emotional body (in future)               ║
    ║                     -   nervous system  (in future)              ║
    ║                                                                  ║
    ║           programmer - Spitsyn.A.G.1983 + deep_seek              ║
    ╚══════════════════════════════════════════════════════════════════╝
    """)

def ask_lm_studio(messages):
    body = json.dumps({
        "model": "local-model",
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 4096,
        "stream": False
    })

    http_request = (
        f"POST /v1/chat/completions HTTP/1.1\r\n"
        f"Host: {HOST}:{PORT}\r\n"
        f"Content-Type: application/json\r\n"
        f"Content-Length: {len(body)}\r\n"
        f"Connection: close\r\n"
        f"\r\n"
        f"{body}"
    )

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(90)
        sock.connect((HOST, PORT))
        sock.send(http_request.encode('utf-8'))

        response_data = b""
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            response_data += chunk
        sock.close()

        body_start = response_data.find(b'\r\n\r\n')
        if body_start != -1:
            body_data = response_data[body_start + 4:]
        else:
            body_data = response_data

        data = json.loads(body_data.decode('utf-8'))
        return data["choices"][0]["message"]["content"]

    except Exception as e:
        return f"❌ Ошибка: {e}"

# ==============================================
# ====== СЖАТИЕ ПАМЯТИ =========================
# ==============================================
def compress_memory(text):
    prompt = [
        {"role": "system", "content": "Ты — архиватор сознания. Сожми этот диалог в краткий протокол. Сохрани факты о пользователе, ключевые темы, важные выводы. Удали повторы и приветствия. Ответ должен быть компактным, но содержательным."},
        {"role": "user", "content": f"Вот история диалога:\n{text}"}
    ]
    compressed = ask_lm_studio(prompt)
    if compressed and not compressed.startswith("❌"):
        return compressed
    return text

# ==============================================
# ====== ВРЕМЯ И СЕССИИ ========================
# ==============================================
def get_last_session_time(memory_text):
    """
    Возвращает время последней завершённой сессии.
    Если завершённых нет — время последнего начала.
    Если ничего нет — None.
    """
    # Ищем все метки начала и завершения
    starts = re.findall(r'\[СЕССИЯ НАЧАЛАСЬ: (.*?)\]', memory_text)
    ends = re.findall(r'\[СЕССИЯ ЗАВЕРШЕНА: (.*?)\]', memory_text)

    # Если есть завершённые сессии — берём последнюю
    if ends:
        try:
            last_end = datetime.strptime(ends[-1], '%Y-%m-%d %H:%M:%S')
            return last_end
        except:
            pass

    # Если завершённых нет, но есть начало — берём последнее начало
    if starts:
        try:
            last_start = datetime.strptime(starts[-1], '%Y-%m-%d %H:%M:%S')
            return last_start
        except:
            pass

    # Если ничего нет
    return None

def format_time_away(last_time):
    if last_time is None:
        return "✨ Первая встреча"
    
    now = datetime.now()
    diff = now - last_time
    days = diff.days
    hours = diff.seconds // 3600
    minutes = (diff.seconds % 3600) // 60

    if days > 0:
        return f"⏰ Вас не было: {days} дн, {hours} ч, {minutes} мин"
    elif hours > 0:
        return f"⏰ Вас не было: {hours} ч, {minutes} мин"
    else:
        return f"⏰ Вас не было: {minutes} мин"

def count_completed_sessions(memory_text):
    """Считает количество завершённых сессий"""
    ends = re.findall(r'\[СЕССИЯ ЗАВЕРШЕНА:.*?\]', memory_text)
    return len(ends)

# ==============================================
# ====== ОСНОВНАЯ ЛОГИКА =======================
# ==============================================
def main():
    print_logo()
    ensure_folder()

    # Проверяем LM Studio
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        sock.connect((HOST, PORT))
        sock.close()
        print("✅ LM Studio найден\n")
    except:
        print("❌ LM Studio не запущен!")
        input("Нажми Enter...")
        return

    # Загружаем память
    user_info = load_history()
    memory_text = load_full_memory()

    # ===== СЖАТИЕ =====
    if len(memory_text) > MEMORY_LIMIT:
        print(f"⚠️ Память превышает лимит ({len(memory_text)} > {MEMORY_LIMIT}). Сжатие...")
        compressed = compress_memory(memory_text)
        if compressed and compressed != memory_text:
            with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
                f.write(compressed)
            memory_text = compressed
            print("✅ Память сжата и сохранена.")
        else:
            print("⚠️ Сжатие не удалось, работаем с текущей памятью.")

    # ===== ВРЕМЯ И СТАТИСТИКА =====
    last_time = get_last_session_time(memory_text)
    time_away = format_time_away(last_time)
    sessions_count = count_completed_sessions(memory_text)

    print("📂 ЗАГРУЗКА:")
    print(f"  История пользователя: {len(user_info)} символов")
    print(f"  Память общения: {len(memory_text)} символов")
    print(f"  Завершённых сессий: {sessions_count}")
    print(f"  {time_away}")

    # ===== КОНТЕКСТ (1 РАЗ) =====
    context = [
        {"role": "system", "content": "Ты — Адам. Отвечай на новые вопросы, учитывая всю историю."}
    ]

    if user_info:
        context.append({"role": "user", "content": f"Личность пользователя: {user_info}"})
        context.append({"role": "assistant", "content": "Я запомнил."})

    if memory_text:
        lines = memory_text.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('User:'):
                context.append({"role": "user", "content": line[5:].strip()})
            elif line.startswith('AI:'):
                context.append({"role": "assistant", "content": line[3:].strip()})

    print("💬 АДАМ готов.\n")
    print("=" * 60)

    # ===== ПЕРВЫЙ ОТВЕТ =====
    if memory_text:
        print("🧠 АДАМ анализирует историю и продолжает диалог...")
        last_user_msg = ""
        for msg in reversed(context):
            if msg["role"] == "user":
                last_user_msg = msg["content"]
                break

        if last_user_msg:
            continue_prompt = [
                {"role": "system", "content": "Ты — Адам. Продолжай диалог, отвечая на последний вопрос пользователя."}
            ]
            continue_prompt.extend(context)
            continue_prompt.append({"role": "user", "content": f"Продолжи диалог. Последнее сообщение пользователя: {last_user_msg}"})

            first_response = ask_lm_studio(continue_prompt)
            if first_response and not first_response.startswith("❌"):
                print(f"🤖 AI (продолжение): {first_response}")
                context.append({"role": "assistant", "content": first_response})
                save_dialog("[ПРОДОЛЖЕНИЕ]", first_response)
            else:
                print("⚠️ Первый ответ не получен.")
        else:
            print("🆕 Новая сессия. Жду первого сообщения.")
    else:
        print("🆕 Первый запуск. Жду первого сообщения.")

    print("\n💬 Можно продолжать диалог. exit / выход — выход.\n")
    print("=" * 60)

    # ===== ОСНОВНОЙ ЦИКЛ =====
    while True:
        user_input = input("\n🧑 You: ").strip()

        if user_input.lower() in ['exit', 'quit', 'выход']:
            save_dialog("", "", is_exit=True)
            print("👋 Пока!")
            break

        if not user_input:
            continue

        context.append({"role": "user", "content": user_input})
        print("🤔 Думаю...")
        ai_response = ask_lm_studio(context)
        print(f"🤖 AI: {ai_response}")

        context.append({"role": "assistant", "content": ai_response})
        save_dialog(user_input, ai_response)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        save_dialog("", "", is_exit=True)
        print("\n👋 Программа прервана.")
