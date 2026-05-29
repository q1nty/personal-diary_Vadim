from flask import Flask, render_template, request, redirect, url_for
import json
import os
from datetime import datetime

app = Flask(__name__)
FILE_NAME = 'entries.json'

def load_entries():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_entries(entries):
    with open(FILE_NAME, 'w', encoding='utf-8') as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)

entries = load_entries()

@app.route('/')
def index():
    return render_template('index.html', entries=entries)

@app.route('/entry/<int:entry_id>')
def detail(entry_id):
    if 0 <= entry_id < len(entries):
        return render_template('detail.html', entry=entries[entry_id], entry_id=entry_id)
    return "Запись не найдена", 404

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        if title and content:
            new_entry = {
                'id': len(entries) + 1,
                'title': title,
                'content': content,
                'date': datetime.now().strftime('%Y-%m-%d %H:%M')
            }
            entries.append(new_entry)
            save_entries(entries)
            return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:entry_id>', methods=['GET', 'POST'])
def edit(entry_id):
    if not (0 <= entry_id < len(entries)):
        return "Запись не найдена", 404
    entry = entries[entry_id]
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        if title and content:
            entry['title'] = title
            entry['content'] = content
            entry['date'] = datetime.now().strftime('%Y-%m-%d %H:%M') + ' (изменено)'
            save_entries(entries)
            return redirect(url_for('index'))
    return render_template('edit.html', entry=entry, entry_id=entry_id)

@app.route('/delete/<int:entry_id>', methods=['POST'])
def delete(entry_id):
    if 0 <= entry_id < len(entries):
        entries.pop(entry_id)
        save_entries(entries)
    return redirect(url_for('index'))

@app.route('/search')
def search():
    query = request.args.get('q', '').strip().lower()
    if query:
        filtered = [e for e in entries if query in e['title'].lower()]
    else:
        filtered = entries
    return render_template('index.html', entries=filtered)

if __name__ == '__main__':
    app.run(debug=True)