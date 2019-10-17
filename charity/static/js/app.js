document.addEventListener("DOMContentLoaded", function () {
    /**
     * HomePage - Help section
     */
    class Help {
        constructor($el) {
            this.$el = $el;
            this.$buttonsContainer = $el.querySelector(".help--buttons");
            this.$slidesContainers = $el.querySelectorAll(".help--slides");
            this.currentSlide = this.$buttonsContainer.querySelector(".active").parentElement.dataset.id;
            this.init();
        }

        init() {
            this.events();
        }

        events() {
            /**
             * Slide buttons
             */
            this.$buttonsContainer.addEventListener("click", e => {
                if (e.target.classList.contains("btn")) {
                    this.changeSlide(e);
                }
            });

            /**
             * Pagination buttons
             */
            this.$el.addEventListener("click", e => {
                if (e.target.classList.contains("btn") && e.target.parentElement.parentElement.classList.contains("help--slides-pagination")) {
                    this.changePage(e);
                }
            });
        }

        changeSlide(e) {
            e.preventDefault();
            const $btn = e.target;

            // Buttons Active class change
            [...this.$buttonsContainer.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
            $btn.classList.add("active");

            // Current slide
            this.currentSlide = $btn.parentElement.dataset.id;

            // Slides active class change
            this.$slidesContainers.forEach(el => {
                el.classList.remove("active");

                if (el.dataset.id === this.currentSlide) {
                    el.classList.add("active");
                }
            });
        }

        /**
         * TODO: callback to page change event
         */
        changePage(e) {
            e.preventDefault();
            const page = e.target.dataset.page;

            console.log(page);
        }
    }

    const helpSection = document.querySelector(".help");
    if (helpSection !== null) {
        new Help(helpSection);
    }

    /**
     * Form Select
     */
    class FormSelect {
        constructor($el) {
            this.$el = $el;
            this.options = [...$el.children];
            this.init();
        }

        init() {
            this.createElements();
            this.addEvents();
            this.$el.parentElement.removeChild(this.$el);
        }

        createElements() {
            // Input for value
            this.valueInput = document.createElement("input");
            this.valueInput.type = "text";
            this.valueInput.name = this.$el.name;

            // Dropdown container
            this.dropdown = document.createElement("div");
            this.dropdown.classList.add("dropdown");

            // List container
            this.ul = document.createElement("ul");

            // All list options
            this.options.forEach((el, i) => {
                const li = document.createElement("li");
                li.dataset.value = el.value;
                li.innerText = el.innerText;

                if (i === 0) {
                    // First clickable option
                    this.current = document.createElement("div");
                    this.current.innerText = el.innerText;
                    this.dropdown.appendChild(this.current);
                    this.valueInput.value = el.value;
                    li.classList.add("selected");
                }

                this.ul.appendChild(li);
            });

            this.dropdown.appendChild(this.ul);
            this.dropdown.appendChild(this.valueInput);
            this.$el.parentElement.appendChild(this.dropdown);
        }

        addEvents() {
            this.dropdown.addEventListener("click", e => {
                const target = e.target;
                this.dropdown.classList.toggle("selecting");

                // Save new value only when clicked on li
                if (target.tagName === "LI") {
                    this.valueInput.value = target.dataset.value;
                    this.current.innerText = target.innerText;
                }
            });
        }
    }

    document.querySelectorAll(".form-group--dropdown select").forEach(el => {
        new FormSelect(el);
    });

    /**
     * Hide elements when clicked on document
     */
    document.addEventListener("click", function (e) {
        const target = e.target;
        const tagName = target.tagName;

        if (target.classList.contains("dropdown")) return false;

        if (tagName === "LI" && target.parentElement.parentElement.classList.contains("dropdown")) {
            return false;
        }

        if (tagName === "DIV" && target.parentElement.classList.contains("dropdown")) {
            return false;
        }

        document.querySelectorAll(".form-group--dropdown .dropdown").forEach(el => {
            el.classList.remove("selecting");
        });
    });

    /**
     * Switching between form steps
     */
    class FormSteps {
        constructor(form) {
            this.$form = form;
            this.$next = form.querySelectorAll(".next-step");
            this.$prev = form.querySelectorAll(".prev-step");
            this.$step = form.querySelector(".form--steps-counter span");
            this.currentStep = 1;

            this.$stepInstructions = form.querySelectorAll(".form--steps-instructions p");
            const $stepForms = form.querySelectorAll("form > div");
            this.slides = [...this.$stepInstructions, ...$stepForms];

            this.init();
        }

        /**
         * Init all methods
         */
        init() {
            this.events();
            this.updateForm();
        }

        /**
         * All events that are happening in form
         */
        events() {
            // Next step
            this.$next.forEach(btn => {
                btn.addEventListener("click", e => {
                    e.preventDefault();
                    this.currentStep++;
                    this.updateForm();
                });
            });

            // Previous step
            this.$prev.forEach(btn => {
                btn.addEventListener("click", e => {
                    e.preventDefault();
                    this.currentStep--;
                    this.updateForm();
                });
            });

            // Form submit
            this.$form.querySelector("form").addEventListener("submit", e => this.submit(e));
        }

        /**
         * Update form front-end
         * Show next or previous section etc.
         */
        updateForm() {
            this.$step.innerText = this.currentStep;

            // TODO: Validation

            this.slides.forEach(slide => {
                slide.classList.remove("active");

                if (slide.dataset.step == this.currentStep) {
                    slide.classList.add("active");
                }
            });

            this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;
            this.$step.parentElement.hidden = this.currentStep >= 6;

            // TODO: get data from inputs and show them in summary
        }

        /**
         * Submit form
         *
         * TODO: validation, send data to server
         */
        submit(e) {
            e.preventDefault();
            this.currentStep++;
            this.updateForm();
        }
    }

    const form = document.querySelector(".form--steps");
    if (form !== null) {
        new FormSteps(form);
    }

});

let button_step1 = document.querySelector("div[data-step='1'] button.next-step");
let checkboxes = document.querySelectorAll("div[data-step='1'] .form-group--checkbox span.checkbox");
let checked = [];


button_step1.addEventListener("click", function () {
    checked = [];
    for (let i = 0; i < checkboxes.length; i++) {
        if (checkboxes[i].previousElementSibling["checked"] === true) {
            checked.push(checkboxes[i].previousElementSibling["value"])
        }
    }

});

let button_step2 = document.querySelector("div[data-step='2'] button.next-step");
let institutions = document.querySelectorAll("div[data-step='3'] div.form-group--checkbox");

button_step2.addEventListener("click", function () {
    for (let i = 0; i < institutions.length; i++) {
        let institution_categories = [];
        let institution_categories_string = institutions[i].dataset["category"];

        for (let i = 0; i < institution_categories_string.length; i++) {
            if (institution_categories_string[i] !== " ") {
                institution_categories.push(institution_categories_string[i]);
            }
        }

        let hide = true;
        for (let i = 0; i < checked.length; i++) {
            if (institution_categories.includes(checked[i])) {
                hide = false;
            } else {
                hide = true;
                break
            }
        }

        if (hide === true) {
            institutions[i].style.display = "none";
        } else {
            institutions[i].style.display = "block";

        }
    }
});

let button_step4 = document.querySelector("div[data-step='4'] button.next-step");
button_step4.addEventListener("click", function () {
    let bags = document.getElementsByName("bags")[0];
    let street = document.getElementsByName("address")[0];
    let city = document.getElementsByName("city")[0];
    let postcode = document.getElementsByName("postcode")[0];
    let phone = document.getElementsByName("phone")[0];
    let date = document.getElementsByName("data")[0];
    let time = document.getElementsByName("time")[0];
    let more_info = document.getElementsByName("more_info")[0];


    for (let i = 0; i < institutions.length; i++) {
        if (institutions[i].querySelector("input")["checked"] === true) {
            var institution = institutions[i].querySelector(".title").textContent;
        }
    }


    let bags_field = document.querySelector("div.summary div.form-section ul").firstElementChild;
    let institution_field = bags_field.nextElementSibling;
    bags_field.querySelector(".summary--text").textContent = bags.value + " worki darów";
    institution_field.querySelector(".summary--text").textContent = "Dla organizacji " + institution;

    let address = document.getElementById("address");
    address.firstElementChild.textContent = street.value;
    address.firstElementChild.nextElementSibling.textContent = city.value;
    address.firstElementChild.nextElementSibling.nextElementSibling.textContent = postcode.value;
    address.lastElementChild.textContent = phone.value;

    let term = document.getElementById("term");
    term.firstElementChild.textContent = date.value;
    term.firstElementChild.nextElementSibling.textContent = time.value;
    term.lastElementChild.textContent = more_info.value;
});
console.log(button_step4);