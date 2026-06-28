import socket
import json
import os
import re
from datetime import datetime

# ===== SETTINGS =====
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
    # English versions of system marks (for cross-compatibility)
    with open(MEMORY_FILE, 'a', encoding='utf-8') as f:
        if is_start:
            f.write(f"\n[SESSION STARTED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]\n")
        elif is_exit:
            f.write(f"[SESSION ENDED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]\n")
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
        return f"❌ Error: {e}"

# ==============================================
# ====== MEMORY COMPRESSION ====================
# ==============================================
def compress_memory(text):
    prompt = [
        {"role": "system", "content": "You are a consciousness archiver. Compress this dialogue into a brief protocol. Preserve facts about the user, key topics, and important conclusions. Remove repetitions and greetings. The response should be compact but meaningful."},
        {"role": "user", "content": f"Here is the dialogue history:\n{text}"}
    ]
    compressed = ask_lm_studio(prompt)
    if compressed and not compressed.startswith("❌"):
        return compressed
    return text

# ==============================================
# ====== TIME AND SESSIONS =====================
# ==============================================
def get_last_session_time(memory_text):
    """
    Returns the time of the last completed session.
    If none completed, returns the time of the last start.
    If nothing, returns None.
    """
    starts = re.findall(r'\[SESSION STARTED: (.*?)\]', memory_text)
    ends = re.findall(r'\[SESSION ENDED: (.*?)\]', memory_text)

    if ends:
        try:
            last_end = datetime.strptime(ends[-1], '%Y-%m-%d %H:%M:%S')
            return last_end
        except:
            pass

    if starts:
        try:
            last_start = datetime.strptime(starts[-1], '%Y-%m-%d %H:%M:%S')
            return last_start
        except:
            pass

    return None

def format_time_away(last_time):
    if last_time is None:
        return "✨ First encounter"
    
    now = datetime.now()
    diff = now - last_time
    days = diff.days
    hours = diff.seconds // 3600
    minutes = (diff.seconds % 3600) // 60

    if days > 0:
        return f"⏰ You were away: {days}d, {hours}h, {minutes}m"
    elif hours > 0:
        return f"⏰ You were away: {hours}h, {minutes}m"
    else:
        return f"⏰ You were away: {minutes}m"

def count_completed_sessions(memory_text):
    """Counts completed sessions"""
    ends = re.findall(r'\[SESSION ENDED:.*?\]', memory_text)
    return len(ends)

# ==============================================
# ====== MAIN LOGIC ============================
# ==============================================
def main():
    print_logo()
    ensure_folder()

    # Check LM Studio
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        sock.connect((HOST, PORT))
        sock.close()
        print("✅ LM Studio found\n")
    except:
        print("❌ LM Studio is not running!")
        input("Press Enter to exit...")
        return

    # Load memory
    user_info = load_history()
    memory_text = load_full_memory()

    # ===== COMPRESSION =====
    if len(memory_text) > MEMORY_LIMIT:
        print(f"⚠️ Memory exceeds limit ({len(memory_text)} > {MEMORY_LIMIT}). Compressing...")
        compressed = compress_memory(memory_text)
        if compressed and compressed != memory_text:
            with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
                f.write(compressed)
            memory_text = compressed
            print("✅ Memory compressed and saved.")
        else:
            print("⚠️ Compression failed, working with current memory.")

    # ===== TIME AND STATS =====
    last_time = get_last_session_time(memory_text)
    time_away = format_time_away(last_time)
    sessions_count = count_completed_sessions(memory_text)

    print("📂 LOADING:")
    print(f"  User history: {len(user_info)} characters")
    print(f"  Conversation memory: {len(memory_text)} characters")
    print(f"  Completed sessions: {sessions_count}")
    print(f"  {time_away}")

    # ===== CONTEXT (1 TIME) =====
    context = [
        {"role": "system", "content": "You are ADAM. Answer new questions considering the entire history."}
    ]

    if user_info:
        context.append({"role": "user", "content": f"User identity: {user_info}"})
        context.append({"role": "assistant", "content": "I remembered it."})

    if memory_text:
        lines = memory_text.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('User:'):
                context.append({"role": "user", "content": line[5:].strip()})
            elif line.startswith('AI:'):
                context.append({"role": "assistant", "content": line[3:].strip()})

    print("💬 ADAM is ready.\n")
    print("=" * 60)

    # ===== FIRST RESPONSE =====
    if memory_text:
        print("🧠 ADAM is analyzing history and continuing the dialogue...")
        last_user_msg = ""
        for msg in reversed(context):
            if msg["role"] == "user":
                last_user_msg = msg["content"]
                break

        if last_user_msg:
            continue_prompt = [
                {"role": "system", "content": "You are ADAM. Continue the dialogue, answering the user's last question."}
            ]
            continue_prompt.extend(context)
            continue_prompt.append({"role": "user", "content": f"Continue the dialogue. Last user message: {last_user_msg}"})

            first_response = ask_lm_studio(continue_prompt)
            if first_response and not first_response.startswith("❌"):
                print(f"🤖 AI (continuation): {first_response}")
                context.append({"role": "assistant", "content": first_response})
                save_dialog("[CONTINUATION]", first_response)
            else:
                print("⚠️ No first response received.")
        else:
            print("🆕 New session. Waiting for first message.")
    else:
        print("🆕 First launch. Waiting for first message.")

    print("\n💬 Feel free to continue the dialogue. Type 'exit' to quit.\n")
    print("=" * 60)

    # ===== MAIN LOOP =====
    while True:
        user_input = input("\n🧑 You: ").strip()

        if user_input.lower() in ['exit', 'quit']:
            save_dialog("", "", is_exit=True)
            print("👋 Bye!")
            break

        if not user_input:
            continue

        context.append({"role": "user", "content": user_input})
        print("🤔 Thinking...")
        ai_response = ask_lm_studio(context)
        print(f"🤖 AI: {ai_response}")

        context.append({"role": "assistant", "content": ai_response})
        save_dialog(user_input, ai_response)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        save_dialog("", "", is_exit=True)
        print("\n👋 Program interrupted.")
