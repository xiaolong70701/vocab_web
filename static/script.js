let currentCard = 0;
const cards = document.querySelectorAll('.flashcard');

function showCard(index) {
    cards.forEach((card, i) => {
        card.style.display = i === index ? 'block' : 'none';
    });
}

document.getElementById('prev').addEventListener('click', () => {
    if (currentCard > 0) {
        currentCard--;
        showCard(currentCard);
    }
});

document.getElementById('next').addEventListener('click', () => {
    if (currentCard < cards.length - 1) {
        currentCard++;
        showCard(currentCard);
    }
});

// 初始化顯示第一張卡片
showCard(currentCard);
