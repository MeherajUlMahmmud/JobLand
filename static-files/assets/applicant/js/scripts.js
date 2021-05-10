(function ($) {
    "use strict"; // Start of use strict

    // Smooth scrolling using jQuery easing
    $('a.js-scroll-trigger[href*="#"]:not([href="#"])').click(function () {
        if (
            location.pathname.replace(/^\//, "") ==
            this.pathname.replace(/^\//, "") &&
            location.hostname == this.hostname
        ) {
            var target = $(this.hash);
            target = target.length
                ? target
                : $("[name=" + this.hash.slice(1) + "]");
            if (target.length) {
                $("html, body").animate(
                    {
                        scrollTop: target.offset().top,
                    },
                    1000,
                    "easeInOutExpo"
                );
                return false;
            }
        }
    });

    // Closes responsive menu when a scroll trigger link is clicked
    $(".js-scroll-trigger").click(function () {
        $(".navbar-collapse").collapse("hide");
    });

    // Activate scrollspy to add active class to navbar items on scroll
    $("body").scrollspy({
        target: "#sideNav",
    });
})(jQuery); // End of use strict


class StarRating extends HTMLElement {

    get value() {
        return this.getAttribute('value');
    }

    set value(val) {

        this.setAttribute('value', val);


        if (val.includes(".")) {
            this.highlight(this.value - 1);
            this.highlightHalf(this.value);


        } else {
            this.highlight(val - 1);
        }


    }

    highlight(index) {
        this.stars.forEach((star, i) => {
            star.classList.toggle('full', i <= index);
        });
    }

    highlightHalf(index) {
        this.stars.forEach((star, i) => {
            star.classList.toggle('fraction', (i > index - 1 && i < index + 1));
        });
    }

    constructor() {
        super();
        this.stars = [];

        for (let i = 0; i < 5; i++) {
            let s = document.createElement('div');
            s.className = 'star';
            this.appendChild(s);
            this.stars.push(s);
        }
        this.value = this.value;


    }
}

window.customElements.define('x-star-rating', StarRating);

var star = 0;

class StarRatingForm extends HTMLElement {


    highlight(index) {
        this.stars.forEach((star, i) => {
            star.classList.toggle('full', i <= index);
        });
    }

    constructor() {
        super();
        this.stars = [];

        for (let i = 0; i < 5; i++) {
            let s = document.createElement('div');
            s.className = 'starform';
            this.appendChild(s);
            this.stars.push(s);
        }
        this.value = this.value;

        this.addEventListener('click', e => {
            let box = this.getBoundingClientRect(),
                starIndex = Math.floor((e.pageX - box.left) / box.width * this.stars.length);

            console.log(starIndex);

            this.highlight(starIndex);
            this.value = starIndex + 1;
            star = this.value;

        })


    }

}

window.customElements.define('x-star-rating-form', StarRatingForm);

function getStar() {
    document.getElementById("ratee").value = star;
}




