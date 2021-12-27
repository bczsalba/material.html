/* Generated using Material.html */

var language = localStorage.getItem("language") || "en";
var darkModeToggle = document.getElementById("dark-mode-toggle");
var previousScroll = 0;
var scrollUpBuffer = 0;
const header = document.querySelector("header");

function toggleLanguage() {
    content_parent = document.getElementById("content-parent")
    language = (language == "en") ? "hu" : "en";
    
    unhideLanguage(language)
    localStorage.setItem("language", language);
    console.log(language);
}

function unhideLanguage(lang) {
    document.body.style.display = "none";

    hu = document.querySelectorAll(".hu")
    en = document.querySelectorAll(".en")

    if (lang == "en") {
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

    else if (lang == "hu") {
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
    };
    document.body.style.display = "block";
}

function toggleDark(transition=true) {
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

const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches

// Set initial data
detectDarkreader();

// Only display content once all images have loaded, apply saved preferences
window.addEventListener("load", (e) => {
    unhideLanguage(language);

    if (localStorage.getItem("isDarkMode") == "true" && prefersDark) {
        toggleDark(false);
    }

    document.getElementById("content-parent").classList.add("show");

    // Update dark mode onchange
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
        if (e.matches && localStorage.getItem("isDarkMode") == "false" 
            || !e.matches && localStorage.getItem("isDarkMode") == "true"
        ) {
            toggleDark();
        }
    });
});

// Detect darkreader on page mutation
new MutationObserver(detectDarkreader).observe(document.querySelector("head"), { childList: true });

window.addEventListener("scroll", () => {
    let scroll = this.scrollY;

    if (scroll < previousScroll) {
        scrollUpBuffer += previousScroll - scroll
    } else {
        scrollUpBuffer = 0;
    };

    if (scroll > 58 && scrollUpBuffer < 15) {
        header.classList.add("collapsed");
    } else if (header.classList.contains("collapsed")) {
        header.classList.remove("collapsed");
    }

    previousScroll = scroll;
});
