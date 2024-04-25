


var navLinks = document.getElementById("navLinks");
function showMenu(){
    navLinks.style.right = "0";
}
function hideMenu(){
    navLinks.style.right = "-250px";
}

function redirectToCalendar() {
    // Redirect to the calendar page
    window.location.href = "/calendar";
}

function redirectToabout() {
    // Redirect to the calendar page
    window.location.href = "/about";
}