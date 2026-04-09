document.getElementById('searchBtn').addEventListener('click', performSearch);
document.getElementById('username').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') performSearch();
});

async function performSearch() {
    const usernameInput = document.getElementById('username');
    const username = usernameInput.value;
    
    // UI Elements
    const errorConsole = document.getElementById('errorConsole');
    const errorMessage = document.getElementById('errorMessage');
    const tableContainer = document.getElementById('tableContainer');
    const resultBody = document.getElementById('resultBody');
    const currentQuery = document.getElementById('currentQuery');
    const noResult = document.getElementById('noResult');

    // Reset UI state
    errorConsole.classList.add('hidden');
    tableContainer.classList.add('hidden');
    noResult.classList.add('hidden');
    resultBody.innerHTML = '';
    
    if (!username) {
        currentQuery.textContent = '-- Waiting for input --';
        return;
    }

    try {
        // 백엔드 API 호출 (username을 쿼리 스트링으로 전달)
        const response = await fetch(`/search?username=${encodeURIComponent(username)}`);
        const result = await response.json();

        // 서버에서 실행된 쿼리 표시
        currentQuery.textContent = result.query;

        if (response.ok) {
            // 성공 시 결과 렌더링
            if (result.data.length > 0) {
                tableContainer.classList.remove('hidden');
                result.data.forEach(row => {
                    const tr = document.createElement('tr');
                    tr.innerHTML = `
                        <td>${row.id}</td>
                        <td>${row.username}</td>
                        <td>${row.email}</td>
                        <td>${row.role}</td>
                    `;
                    resultBody.appendChild(tr);
                });
            } else {
                noResult.classList.remove('hidden');
            }
        } else {
            // 서버 에러(500) 발생 시 (SQL Injection 성공 시 에러 유도)
            throw new Error(result.message);
        }
    } catch (err) {
        // SQL 에러 콘솔에 출력
        errorConsole.classList.remove('hidden');
        errorMessage.textContent = err.message;
        console.error('Database Error:', err.message);
    }
}
