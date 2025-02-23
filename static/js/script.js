// NAVIGACE -------------------------------------------------------------------

const toggleBtn = document.querySelector(".toggle-btn");
const toggleBtnIcon = document.querySelector(".toggle-btn i");
const dropDownMenu = document.querySelector(".dropdown-menu");

toggleBtn.onclick = function () {
	dropDownMenu.classList.toggle("open");
	const isOpen = dropDownMenu.classList.contains("open");

	toggleBtnIcon.classList = isOpen ? "fa-solid fa-xmark" : "fa-solid fa-bars";
};

document.addEventListener("DOMContentLoaded", function () {
	// Najdeme formulář s třídou "contact-form"
	const formular = document.querySelector(".contact-form");

	if (formular) {
		// Najdeme ostatní prvky pro validaci
		const fullName = document.querySelector(".fullName");
		const email = document.querySelector(".email");
		const notifName = document.querySelector(".notifName");
		const notifEmail = document.querySelector(".notifEmail");
		const textareaForm = document.querySelector(".message");
		const p = document.querySelector(".text-counter");

		// Ověříme, zda všechny očekávané prvky existují
		if (fullName && email && notifName && notifEmail && textareaForm && p) {
			// Odeslání formuláře s validací
			formular.addEventListener("submit", (event) => {
				event.preventDefault();
				// Skryjeme starší upozornění
				notifName.style.display = "none";
				notifEmail.style.display = "none";

				let hasError = false;

				// Kontrola jména
				if (fullName.value.trim() === "") {
					notifName.textContent = "Vyplňte jméno a příjmení";
					notifName.style.display = "block";
					hasError = true;
				}

				// Kontrola e-mailu
				const emailValue = email.value.trim().toLowerCase();
				if (emailValue === "") {
					notifEmail.textContent = "Vyplňte email";
					notifEmail.style.display = "block";
					hasError = true;
				} else {
					const endsWithCZorCOM = /\.(cz|com)$/i.test(emailValue);
					if (!endsWithCZorCOM) {
						notifEmail.textContent =
							"Email musí končit na .cz nebo .com";
						notifEmail.style.display = "block";
						hasError = true;
					}
				}

				// Pokud nejsou chyby, odešleme formulář
				if (!hasError) {
					formular.submit();
				}
			});

			// Skrytí upozornění při psaní do pole jméno
			fullName.addEventListener("input", () => {
				if (fullName.value.trim() !== "") {
					notifName.style.display = "none";
				}
			});

			// Skrytí upozornění při psaní do pole e-mail
			email.addEventListener("input", () => {
				if (email.value.trim() !== "") {
					notifEmail.style.display = "none";
				}
			});

			// Počítadlo znaků v textarea
			textareaForm.addEventListener("input", () => {
				const lettersCount = textareaForm.value.length;

				if (lettersCount >= 150) {
					textareaForm.style.color = "red";
					p.style.color = "red";
				} else if (lettersCount >= 90 && lettersCount < 150) {
					textareaForm.style.color = "orange";
					p.style.color = "orange";
				} else {
					textareaForm.style.color = "black";
					p.style.color = "black";
				}

				p.textContent = lettersCount;
			});
		} else {
			console.log(
				"Formulář neobsahuje očekávané prvky pro validaci. Kód se neprovede."
			);
		}
	}
});
// Tlačítko zpět nahoru -----------------------------------------------------
// // Vybereme tlačítko pomocí jeho ID
const topButton = document.getElementById("top-button");

// Přidáme posluchač událostí na okno pro sledování scrollování
window.addEventListener("scroll", () => {
	if (window.scrollY >= 100) {
		topButton.style.display = "block"; // Zobrazíme tlačítko
	} else {
		topButton.style.display = "none"; // Skryjeme tlačítko
	}
});

// Přidáme posluchač událostí na tlačítko pro plynulé posouvání na vrchol stránky
topButton.addEventListener("click", () => {
	window.scrollTo({
		top: 0,
		behavior: "smooth", // Plynulé posouvání
	});
});
// --------------------------------------------------------------------------------

//=============================================
// SPARE_PARTS.HTML KOD PRO SWIPER POSUN FOTEK
//=============================================

document.addEventListener("DOMContentLoaded", function () {
	document.querySelectorAll(".spare-parts-slider").forEach(function (slider) {
		let slides = slider.querySelectorAll(".swiper-slide").length;
		let loopMode = slides > 1; // Loop zapni jen pokud je více než 1 slide

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
