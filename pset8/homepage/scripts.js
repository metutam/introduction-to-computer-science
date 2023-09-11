let counter = 1;

// Toggles visibility of greeting
function blink()
{
    let text = "I'm a Software Engineer";
    let content = document.querySelector('.content');

    if (counter == (text.length + 1))
    {
        content.style.visibility = 'hidden';
        counter = 1;
    }
    else
    {
        document.querySelector('.content').innerHTML = text.slice(0, counter);
        content.style.visibility = 'visible';
        counter++;
    }
}

// Blink every 200ms
window.setInterval(blink, 200);
