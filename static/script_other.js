const noButton = document.getElementById("noButton");
const yesButton = document.getElementById("yesButton");

let clickCount = 0;

noButton.addEventListener("click", function() {
    clickCount++;
    console.log("No Button Clicked. Click Count:", clickCount);
});

yesButton.addEventListener("click", function() {
    console.log("Yes Button Clicked. Sending click count:", clickCount);
    
    fetch('/update_click_count', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ clickCount: clickCount })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log('Server response:', data);
        window.location.href = '/yipeee';
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });
});

noButton.addEventListener("click", function() {
    console.log("qwe");

    let currentHeight = parseFloat(window.getComputedStyle(yesButton, null).getPropertyValue('height'));
    let currentWidth = parseFloat(window.getComputedStyle(yesButton, null).getPropertyValue('width'));
    let currentFontSize = parseFloat(window.getComputedStyle(yesButton, null).getPropertyValue('font-size'));
  
    let newHeight = 1.5 * currentHeight + "px";
    let newWidth = 1.2 * currentWidth + "px";
    let newFontSize = 1.5 * currentFontSize + "px";
  
    yesButton.style.height = newHeight;
    yesButton.style.width = newWidth;
    yesButton.style.fontSize = newFontSize;
  });