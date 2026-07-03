# 🎓 EduGuide AI — Easy Start Guide

This guide explains, in plain everyday language, how to start the EduGuide AI app on your computer. No technical background needed. Just follow the steps in order.

---

## 🧐 What Is This App?

EduGuide AI is a study helper. You give it a PDF (like a textbook chapter or notes), and it can:

- **Summarize** the document into short, easy notes.
- **Answer questions** you ask about the document.
- **Create quizzes** to test what you learned.
- **Track your scores** over time.

It runs in your web browser, but it lives on your own computer.

---

## 🗺️ The Big Picture (What "Starting" Means)

Think of it like cooking a meal:

1. **Ingredients** — the app needs some helper programs installed (already done for you once).
2. **A key** — the app talks to Google's AI. To do that, it needs a password-like "key". You must add your own key.
3. **Turn on the stove** — you run one command, and the app opens in your browser.

That's the whole idea. Below are the exact steps.

---

## ✅ One-Time Setup (Do This Only Once)

You only need to do this section **the very first time**. After that, skip straight to "Starting the App Every Day".

### Step 1 — Open the Terminal

The Terminal is a text window where you type commands.

- Open your file manager, go to the project folder (`projeduguide`).
- Right-click inside the folder → choose **"Open Terminal Here"** (or open the Terminal app and navigate to the folder).

You should see the folder name in the window. Good.

### Step 2 — Install the Helper Programs

The app needs some background programs to work. This has **already been installed** during setup. If someone needs to redo it on a fresh computer, they would run:

```bash
python3 -m venv --without-pip .venv
./.venv/bin/python get-pip.py
./.venv/bin/pip install -r requirements.txt
```

> 💡 In plain words: this creates a private box (`.venv`) that holds all the app's tools, so they don't mess with the rest of your computer. You do **not** need to understand the commands — just know it's the "install ingredients" step.

### Step 3 — Add Your AI Key (Very Important)

The app talks to Google's AI. Google needs to know it's really you, so it gives you a personal **key** (a long secret code).

**Get your key:**

1. Open this website in your browser: **https://aistudio.google.com/apikey**
2. Sign in with your Google account.
3. Click **"Create API Key"**.
4. Copy the long code it gives you. It looks like this: `AIzaSy...` followed by many letters and numbers.

**Put the key into the app:**

1. In the project folder, open the folder called `config`.
2. Open the file named `.env` with any text editor (like Notepad, TextEdit, or VS Code).
3. Find the line that starts with `GEMINI_API_KEY=`.
4. Replace whatever is after the `=` with your new key. It should look like:

   ```
   GEMINI_API_KEY=AIzaSy...your_real_key_here...
   ```

5. **Save** the file.

> ⚠️ **Important:** The key must start with `AIzaSy`. If it starts with anything else, it is the wrong key and the AI features will not work. Keep this key private — treat it like a password.

### Step 4 — Check That Everything Is Ready

Run this in the Terminal:

```bash
./.venv/bin/python verify_setup.py
```

If you see **"🎉 All checks passed!"** at the bottom, you are ready. 🎉

If you see an error about the key being missing, go back to **Step 3**.

---

## 🚀 Starting the App Every Day

Once the one-time setup is done, starting the app is just **one command**.

1. Open the Terminal in the project folder (same as Step 1 above).
2. Type this and press **Enter**:

   ```bash
   ./.venv/bin/streamlit run app/app.py
   ```

3. Wait a few seconds. Your web browser should open automatically to the app.
4. If it does **not** open by itself, look in the Terminal for a line like:

   ```
   Local URL: http://localhost:8501
   ```

   Copy that address (`http://localhost:8501`) and paste it into your browser.

That's it — the app is running! 🎉

---

## 🖥️ How to Use the App

Once it's open in your browser:

1. **Upload a PDF** — on the left side panel, click "Upload course material" and pick a PDF from your computer. Wait for it to finish processing.
2. **Smart Summary & Q&A tab** — click "Generate Contextual Summary" for notes, or type a question in the box to ask about the document.
3. **Interactive Quiz tab** — choose how many questions and the difficulty, click to build the quiz, answer, then submit to see your score.
4. **Performance Analytics tab** — see your past quiz scores and progress over time.

---

## 🛑 How to Stop the App

- Go back to the Terminal window where it is running.
- Press **Ctrl + C** (hold Control, tap C).
- The app stops. Close the browser tab too if you like.

---

## 🆘 If Something Goes Wrong

| What you see | What it means | What to do |
|---|---|---|
| "GEMINI_API_KEY is missing" | The app has no key. | Redo **Step 3** — add your key to `config/.env`. |
| "invalid authentication credentials" | The key is wrong or fake. | Get a real key starting with `AIzaSy` from Google AI Studio (Step 3). |
| Browser doesn't open | Normal sometimes. | Copy `http://localhost:8501` into your browser manually. |
| "command not found" | Terminal is in the wrong folder. | Make sure the Terminal is opened **inside** the `projeduguide` folder. |
| A yellow "deprecation" warning appears | Just a notice, not an error. | Ignore it — the app still works. |

---

## 📌 Quick Reference (Cheat Sheet)

**Start the app:**
```bash
./.venv/bin/streamlit run app/app.py
```

**Stop the app:** press `Ctrl + C` in the Terminal.

**Check setup:**
```bash
./.venv/bin/python verify_setup.py
```

**Your key goes here:** `config/.env` → the `GEMINI_API_KEY=` line.

---

Happy studying! 📚
