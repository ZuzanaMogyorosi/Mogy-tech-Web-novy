// ====================================================================
// 0) NAVIGACE – Otevření/zavření menu pomocí ikonky (hamburger ↔ křížek)
// ====================================================================

const toggleBtn = document.querySelector(".toggle-btn");
const toggleBtnIcon = document.querySelector(".toggle-btn i");
const dropDownMenu = document.querySelector(".dropdown-menu");

toggleBtn.onclick = function () {
	dropDownMenu.classList.toggle("open");
	const isOpen = dropDownMenu.classList.contains("open");

	toggleBtnIcon.classList = isOpen ? "fa-solid fa-xmark" : "fa-solid fa-bars";
};

// ====================================================================
// 1) KONTAKTNÍ FORMULÁŘ – Validace a počítadlo znaků zprávy
// ====================================================================

document.addEventListener("DOMContentLoaded", function () {
	// ─ Formulář a jednotlivé prvky
	const formular = document.querySelector(".contact-form");
	const fullName = document.querySelector(".fullName");
	const email = document.querySelector(".email");
	const notifName = document.querySelector(".notifName");
	const notifEmail = document.querySelector(".notifEmail");
	const textareaForm = document.querySelector(".message");
	const p = document.querySelector(".text-counter");

	// ─ Pokud jsou všechny prvky dostupné
	if (
		formular &&
		fullName &&
		email &&
		notifName &&
		notifEmail &&
		textareaForm &&
		p
	) {
		// ─ Validace při odeslání
		formular.addEventListener("submit", (event) => {
			let hasError = false;

			// Skryjeme staré chybové zprávy
			notifName.style.display = "none";
			notifEmail.style.display = "none";

			// Kontrola jména
			if (fullName.value.trim() === "") {
				notifName.textContent = "Vyplňte jméno a příjmení";
				notifName.style.display = "block";
				hasError = true;
			}

			// Kontrola e-mailu
			const emailValue = email.value.trim().toLowerCase();
			const emailPattern =
				/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.(cz|com|net|org|eu|sk)$/i;
			if (emailValue === "") {
				notifEmail.textContent = "Vyplňte email";
				notifEmail.style.display = "block";
				hasError = true;
			} else if (!emailPattern.test(emailValue)) {
				notifEmail.textContent =
					"Zadejte platný e-mail (např. jmeno@domena.cz)";
				notifEmail.style.display = "block";
				hasError = true;
			}

			// Pokud je chyba, zabráníme odeslání
			if (hasError) {
				event.preventDefault();
			}
		});

		// ─ Skrytí hlášek při psaní
		fullName.addEventListener("input", () => {
			if (fullName.value.trim() !== "") {
				notifName.style.display = "none";
			}
		});
		email.addEventListener("input", () => {
			if (email.value.trim() !== "") {
				notifEmail.style.display = "none";
			}
		});

		// ─ Počítadlo znaků ve zprávě
		textareaForm.addEventListener("input", () => {
			const lettersCount = textareaForm.value.length;
			p.textContent = lettersCount;

			if (lettersCount >= 150) {
				textareaForm.style.color = "red";
				p.style.color = "red";
			} else if (lettersCount >= 90) {
				textareaForm.style.color = "orange";
				p.style.color = "orange";
			} else {
				textareaForm.style.color = "black";
				p.style.color = "black";
			}
		});
	}
});

// ====================================================================
// 2) TLAČÍTKO ZPĚT NAHORU – Viditelnost a scroll zpět
// ====================================================================

const topButton = document.getElementById("top-button");

window.addEventListener("scroll", () => {
	if (window.scrollY >= 100) {
		topButton.style.display = "block";
	} else {
		topButton.style.display = "none";
	}
});

topButton.addEventListener("click", () => {
	window.scrollTo({
		top: 0,
		behavior: "smooth",
	});
});

// ====================================================================
// 3) SWIPER – Dynamické nastavení slideru pro náhradní díly
// ====================================================================

document.addEventListener("DOMContentLoaded", function () {
	document.querySelectorAll(".spare-parts-slider").forEach(function (slider) {
		let slides = slider.querySelectorAll(".swiper-slide").length;
		let loopMode = slides > 1;

		new Swiper(slider, {
			loop: loopMode,
			navigation: {
				nextEl: slider.querySelector(".swiper-button-next"),
				prevEl: slider.querySelector(".swiper-button-prev"),
			},
			autoplay: {
				delay: 6000,
				disableOnInteraction: false,
			},
			slidesPerView: 1,
		});
	});
});
