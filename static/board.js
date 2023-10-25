// 使用Fetch API从后端获取文本数据
fetch('/api/textdata')
  .then(response => response.json())
  .then(data => {
    // 在前端页面上显示文本数据
    const textContainer = document.getElementById('text-container');
    data.forEach(item => {
      const paragraph = document.createElement('p');
      paragraph.textContent = item.text;
      textContainer.appendChild(paragraph);
    });
  })
  .catch(error => console.error('Fetch error: ' + error));
