const textArray = ["Привет, солнышко!!", "Скоро 14 февраля...", "Поэтому...."];
let currentIndex = 0;

const textElement = document.getElementById("welcome-text");
const nextButton = document.getElementById("nextButton");

function changeText() {
  currentIndex = (currentIndex + 1);
  if (currentIndex < textArray.length) {
    textElement.textContent = textArray[currentIndex];
  } else {
    window.location.href = '/change';
  }
}

nextButton.addEventListener("click", changeText);