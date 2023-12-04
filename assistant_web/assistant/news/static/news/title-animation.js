const projectName = "Sgt. Pepper's Lonely Debuggers Club";
const members = ["Розробники:", "Дмитро Гаврильченко - Team lead", "Юрій Сергієнко - Scrum master", "Андрій Вовчок", "Владислав Стельмах", "Ганна Саган"];
const projectDescription = ["Дякуємо за використання 'Особистого помічника' від Sgt. Pepper's Lonely Debuggers Club (R).", "Наша незалежна команда розробників зробила все можливе, щоб створити просту, інтуїтивно зрозумілу програму для щоденного використання для всіх типів користувачів.", "Ми придумали ідею простого веб-додатку, який може спростити повсякденну рутину та поєднати в одному місці більшість завдань, з якими може зіткнутися одна людина в сучасному цифровому світі, наприклад розваги, керування контактами, нотатками та безпечне хмарне зберігання для файлів.", '<br>', "Перший випуск вашої програми підтримує такі завдання:", "* зберігати та редагувати контакти з іменами, адресами, номерами телефонів, електронною поштою та днями народження в книзі контактів;", "* сповіщати про майбутні дні народження;", "* зберігати та редагувати нотатки з вмістом і ключовими словами;", "* завантажувати файли користувача в хмарний сервіс і відображати їх за категоріями;", "* надати короткий огляд місцевих і світових новин за категоріями;", "* для зручності користувачів наш додаток підтримує світлий і темний режими і багатомовний пакет.", '<br>', "При розробці були використані такі технології:", "* Інтерфейс", "- HTML", "- CSS", '<br>', "* Бекенд", "- Python", "- JavaScript", "- Джанго", '<br>', "* Утиліти", "- VSCode", "- Git/GitHub", "- Докер", "- Trello", '<br>', "* Веб-сервіси", "- AWS", "- ElephantSQL", "- Fly.io", '<br>', "Щиро Ваш,", "сержант Pepper's Lonely Debuggers Club (R)"];

const titleElement = document.querySelector('.project-title');
const flipButton = document.querySelector('.flip-text-btn');

let currentText = "";
let index = 0;
let showProjectName = true;
let typingTimeout = null;

function typeText(text) {
    if (index < text.length) {
        currentText += text[index];
        titleElement.innerHTML = currentText;
        index++;
        clearTimeout(typingTimeout);  // Cancel the previous timeout
        typingTimeout = setTimeout(() => typeText(text), 1);  // And let's launch a new one
    }
}

flipButton.addEventListener('click', () => {
    index = 0;
    currentText = "";
    clearTimeout(typingTimeout);  // Cancel the previous timeout
    if (showProjectName) {
        typeText(projectDescription.join('<br>'));
    } else {
        typeText(projectName + '<br><br>' + members.join('<br>'));
    }
    showProjectName = !showProjectName;
});

typeText(projectName + '<br><br>' + members.join('<br>'));
