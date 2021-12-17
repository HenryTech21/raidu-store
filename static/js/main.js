const mySlide = document.querySelectorAll('.mySlider'),
    dot = document.querySelectorAll('.dot');

let counter = 1;
slidemove(counter);

let timer = setInterval(autoslide, 9000);

function autoslide() {
    counter += 1;
    slidemove(counter);
}

function plusSlides(e) {
    counter += e;
    slidemove(counter);
    resetTimer();
}

function currentSlide(e) {
    counter = e;
    slidemove(counter);
    resetTimer();
}

function resetTimer() {
    clearInterval(timer);
    timer = setInterval(autoslide, 8000);
}

function slidemove(e) {
    let i;
    for (i = 0; i < mySlide.length; i++) {
        mySlide[i].style.display = 'none';
    }
    for (i = 0; i < dot.length; i++) {
        dot[i].classList.remove('active');
    }
    if (e > mySlide.length) {
        counter = 1;
    }
    if (e < 1) {
        counter = mySlide.length;
    }
    mySlide[counter - 1].style.display = 'block';
    dot[counter - 1].classList.add('active');
}