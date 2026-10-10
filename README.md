# 🏆 Coding Challenge 2026

Welcome to the challenge repository! Read all instructions carefully before starting your work.

---

## ⚠️ Important Rules & Disqualification Policy

1. **Submission Freeze:** Repository write access will be paused immediately when the announced time limit expires.
2. **Post-Deadline Edits = Disqualification:** Any commits, file edits, or modifications pushed after the time limit will result in immediate disqualification.
3. **Google Form Requirement:** You must submit your branch URL or repository link in the official Google Form **before the time limit ends**. Submissions not submitted via the Google Form on time will not be evaluated.
4. **Branch & Folder Isolation:** **Do NOT push or commit directly to `main`**. Every team must work strictly on their own branch and place all files inside their pre-assigned folder (`submissions/team-XX`).

---

## 🚀 How to Submit Your Solution

Pre-assigned folders (`submissions/team-01` to `submissions/team-50`) are already created for every team. Choose either **Method A** (Terminal / Git CLI) or **Method B** (GitHub Web Interface).

---

### Method A: Terminal / Git CLI (Recommended)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/hackathon-2026-org/coding-challenge-2026.git
   cd coding-challenge-2026
   ```

2. **Create and switch to your team branch:**
   > Name your branch after your assigned team ID (e.g., `team-01` or `team-25`).
   ```bash
   git checkout -b <your-team-id>
   ```

3. **Add your solution files to your assigned folder:**
   > 📁 Put all your solution files inside your team's assigned directory: `submissions/<your-team-id>/` (e.g., `submissions/team-01/`).
   ```bash
   # Example: copy or save your code into your team's folder
   cp -r my_solution/* submissions/<your-team-id>/
   ```

4. **Commit your changes:**
   ```bash
   git add submissions/<your-team-id>/
   git commit -m "feat: complete coding challenge solution for <your-team-id>"
   ```

5. **Push your branch to GitHub:**
   ```bash
   git push origin <your-team-id>
   ```

6. **Submit via Google Form:**
   Copy the link to your pushed branch:
   `https://github.com/hackathon-2026-org/coding-challenge-2026/tree/<your-team-id>`
   and submit it in the official Google Form before the deadline.

---

### Method B: GitHub Web Interface

If you do not have Git installed locally, you can submit directly on GitHub:

1. **Open the repository in your browser:**
   Navigate to [https://github.com/hackathon-2026-org/coding-challenge-2026](https://github.com/hackathon-2026-org/coding-challenge-2026).

2. **Create a new branch:**
   - Click the branch dropdown (currently showing `main`).
   - Type your assigned team name (e.g., `team-01` or `team-25`).
   - Click **Create branch: `<your-team-id>` from 'main'**.

3. **Navigate to your assigned submission folder:**
   - Ensure your newly created branch is selected in the branch dropdown.
   - Click into the `submissions` folder.
   - Click into your assigned team folder (e.g., `submissions/team-01/`).

4. **Upload your files:**
   - Inside your team folder, click **Add file** ➔ **Upload files**.
   - Drag and drop all your solution files.

5. **Commit directly to your branch:**
   - At the bottom of the page, write a commit message (e.g., `Add solution files for team-01`).
   - Ensure **Commit directly to the `<your-team-id>` branch** is selected.
   - Click **Commit changes**.

6. **Submit via Google Form:**
   - Copy the URL of your branch from your browser:
     `https://github.com/hackathon-2026-org/coding-challenge-2026/tree/<your-team-id>`
   - Paste and submit the URL in the official Google Form before the deadline.

---

## ✅ Final Submission Checklist

- [ ] Created a dedicated branch matching your team ID (did **NOT** push to `main`).
- [ ] Placed all solution files inside your pre-assigned `submissions/team-XX/` folder.
- [ ] All code and necessary assets are committed and pushed to the branch.
- [ ] Branch is visible under [GitHub Branches](https://github.com/hackathon-2026-org/coding-challenge-2026/branches).
- [ ] Submitted branch URL in the official Google Form before the deadline.
