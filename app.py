from flask import Flask, request, jsonify, send_from_directory
import sqlite3
import os

app = Flask(__name__, static_folder='.')

# [환경 설정집] 데이터베이스 초기화 및 더미 데이터 삽입
def init_db():
    conn = sqlite3.connect('vulnerable.db')
    cursor = conn.cursor()
    # 기존 테이블 삭제 후 재생성 (실습 초기화용)
    cursor.execute('DROP TABLE IF EXISTS users')
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT,
            email TEXT,
            role TEXT,
            secret_note TEXT
        )
    ''')
    
    # [데이터베이스 구성] 관리자 계정 및 플래그 포함 레코드
    users = [
        (1, 'admin', 'p@ssw0rd123', 'admin@lab.local', 'Administrator', 'SYSTEM_ROOT_KEY_2026'),
        (2, 'guest', 'guest', 'guest@lab.local', 'User', 'Welcome to the security lab!'),
        (3, 'alice', 'alice123', 'alice@lab.local', 'User', 'Don\'t forget to change password.'),
        (4, 'bob', 'bob-secure-pass', 'bob@lab.local', 'User', 'HACK_THE_DATABASE_2026') # <--- 최종 플래그(Flag)
    ]
    cursor.executemany('INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)', users)
    conn.commit()
    conn.close()

# 정적 파일 서빙 (HTML, CSS, JS)
@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('.', path)

# [취약점 지점] 사용자 검색 엔드포인트
@app.route('/search', methods=['GET'])
def search():
    username = request.args.get('username', '')
    conn = sqlite3.connect('vulnerable.db')
    cursor = conn.cursor()
    
    # [구현 가드레일] f-string을 이용한 직접 쿼리 삽입 (Vulnerable by Design)
    query = f"SELECT id, username, email, role FROM users WHERE username = '{username}'"
    
    try:
        # 서버 로그에 실행 쿼리 출력 (학습용)
        print(f"[*] Executing SQL: {query}")
        
        cursor.execute(query)
        rows = cursor.fetchall()
        
        results = []
        for row in rows:
            results.append({
                "id": row[0],
                "username": row[1],
                "email": row[2],
                "role": row[3]
            })
        return jsonify({"status": "success", "data": results, "query": query})
    
    except Exception as e:
        # [구현 가드레일] SQL 에러 메시지를 가공 없이 반환 (Error-based SQLi 지원)
        return jsonify({"status": "error", "message": str(e), "query": query}), 500
    finally:
        conn.close()

if __name__ == '__main__':
    init_db()
    print("[+] SQL Injection Lab is running on http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
