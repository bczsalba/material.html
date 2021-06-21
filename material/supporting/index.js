var language = localStorage.getItem("language");
var darkModeToggle = document.getElementById("dark-mode-toggle");

// Todo: this isn't consistent through different sites
function toggleLanguage(save=false) {
    hu = document.querySelectorAll(".hu")
    en = document.querySelectorAll(".en")
    content_parent = document.getElementById("content-parent")

    language = (language == "en") ? "hu" : "en";
    document.body.style.display = "none"

    if (language == "hu") {
        hu.forEach((element) => {
            element.style.display = "none";
        });
        en.forEach((element) => {
            if (element.parentElement.classList.contains("nav-item")) {
                element.style.display = "inline-block";
            } else {
                element.style.display = "block";
            }
        });
    }

    else if (language == "en") {
        hu.forEach((element) => {
            if (element.parentElement.classList.contains("nav-item")) {
                element.style.display = "inline-block";
            } else {
                element.style.display = "block";
            }

        });
        en.forEach((element) => {
            element.style.display = "none";
        });
    }

    document.body.style.display = "block"
}

function toggleDark(transition=true) {
    // create transition style
    if (transition) {
        style = document.createElement("style")
        style.innerHTML = `
            html, .content {
                transition: all 0.5s;
            }
        `

        if (document.head.contains(style)) {
            document.head.removeChild(style);
        }

        document.head.appendChild(style);
    }

    // toggle the dark-mode class for body
    document.documentElement.classList.toggle("dark-mode");

    // update icon
    if (darkModeToggle.classList.contains("material-icons-outlined")) {
        darkModeToggle.classList.remove("material-icons-outlined");
        darkModeToggle.classList.add("material-icons");
        localStorage.setItem("isDarkMode", true);
    } 
    
    else {
        darkModeToggle.classList.remove("material-icons")
        darkModeToggle.classList.add("material-icons-outlined")
        localStorage.setItem("isDarkMode", false)
    }
}

function detectDarkreader() {
    darkreaderActive = (document.querySelector("head").querySelector('meta[name="darkreader"]') != null);

    if (darkreaderActive) {
        darkModeToggle.style.display = "none"
    } else {
        darkModeToggle.style.display = "inline-block"
    }
}

// Set initial data
detectDarkreader();
toggleLanguage();

// Only display content once all images have loaded
Promise.all(Array.from(document.images)
    .filter(img => !img.complete)
    .map(img => new Promise(resolve => {
        img.onload = img.onerror = resolve;
    }))
).then(() => {
    document.getElementById("content-parent").classList.add("show");
});

// Detect darkreader on page mutation
new MutationObserver(detectDarkreader).observe(document.querySelector("head"), { childList: true });

// Apply saved preferances
window.onload = () => {
    if (localStorage.getItem("isDarkMode") == "true") {
        toggleDark(false);
    };
};
