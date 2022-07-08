import * as api from "./client_api.js";
import * as shopping from "./shopping_cart.js";

class ReservationDisplay {
    constructor(display_element) {
        this.display = document.getElementById(display_element);
        this.cart = new shopping.ShoppingCart();
        this.loading_element = document.getElementById("loading");
        this.reservations = document.getElementById("reservations");
        this.total_price = 0;
        this.price_element = document.getElementById("total_price");

        this.checkout_button = document.getElementById("checkout_button");
        this.checkout_button.addEventListener("click", async (e) => {
            await this.checkout();
        });
    }

    async change_price(amount) {
        /*
         * Changes and sets the total price on the page.
         *
         * Positive values increase the total, negative values decrease the total
         */
        this.total_price += amount;
        this.price_element.innerText = this.total_price;
    }

    async setup() {
        /*
         * This would be a LOT easier if I were able to pass a template HTML
         * element to this somehow. It may very well be possible and I don't
         * know how.
         */

        var date;
        var time;
        var seat;
        var play;
        var selected_element;
        var selected_title;
        var selected_title_p;
        var selected_details;

        for (let i = 0; i < this.cart.contents.length; i++) {
            date = await api.get_date(this.cart.contents[i]['date']);
            time = await api.get_time(this.cart.contents[i]['time']);
            seat = await api.get_seat(this.cart.contents[i]['seat']);
            play = await api.get_play(seat.play);

            selected_element = document.createElement("div");
            selected_element.classList.add("selection");

            selected_title = document.createElement("header");
            selected_title.classList.add("selection_title");

            selected_title_p = document.createElement("p");
            selected_title_p.innerText = play.name;

            selected_title.appendChild(selected_title_p);
            selected_element.appendChild(selected_title);
            this.reservations.appendChild(selected_element);

            selected_details = document.createElement("section");
            selected_details.classList.add("selection_details")

            selected_details.appendChild(await this.seat_element(seat));
            selected_details.appendChild(await this.date_element(date));
            selected_details.appendChild(await this.time_element(time));

            selected_element.appendChild(selected_details);
            selected_element.appendChild(await this.removal_element(seat.id, date.id, time.id))

            this.total_price += parseInt(seat.price);
        }

        this.loading_element.style.display = "none";
        this.price_element.innerText = this.total_price;
    }

    async get_objects(seat_id, date_id, time_id) {
        var seat = await api.get_seat(seat_id);
        var play = await seat.play;
        var date = await api.get_date(date_id);
        var time = await api.get_time(time_id);
    }

    async date_element(date) {
        /*
         * Constructs an HTML block that the date can be placed in.
         */
        var element = document.createElement("p");
        element.innerHTML = `Date: ${date.date}`;
        element.classList.add("selection_date");
        return element;
    }

    async time_element(time) {
        /*
         * Constructs an HTML block that the time can be placed in.
         */
        var element = document.createElement("p");
        element.innerHTML = `Time: ${time.time}`;
        element.classList.add("selection_time");
        return element;
    }

    async seat_element(seat) {
        /*
         * Constructs an HTML block that the seat can be placed in.
         */
        var element = document.createElement("p");
        element.innerHTML = `Price: ${seat.price}`;
        element.classList.add("selection_price");
        return element;
    }

    async removal_element(seat, date, time) {
        /*
         * Generates an element that can be clicked on. Clicking on this element
         * should cause the item to be removed from the cart.
         */
        var element = document.createElement("p");
        var text = document.createElement("span");
        text.innerText = "X";
        element.classList.add("selection_removal");
        text.classList.add("selection_removal_text");
        element.appendChild(text);
        element.setAttribute("seat", seat);
        element.setAttribute("time", time);
        element.setAttribute("date", date);
        text.setAttribute("time", time);
        text.setAttribute("date", date);
        text.setAttribute("seat", seat);
        text.setAttribute("double", true);

        element.addEventListener("click", async (click_event) => {
            await this.remove_seat(click_event);
        });

        return element;
    }

    async remove_seat(click_event) {
        var element = click_event.srcElement
        var seat = element.getAttribute("seat");
        var date = element.getAttribute("date");
        var time = element.getAttribute("time");


        var status = await this.cart.remove(seat, date, time);
        if (! status.error) {
            // Check to see if this is the span element or not. If it's the span
            // element, we need to remove the parent's parent element.
            if (element.getAttribute("double")) {
                element.parentElement.parentElement.remove();
            }
            else {
                element.parentElement.remove();
            }
            seat = await api.get_seat(seat);
            this.change_price(seat.price * -1);
        }
    }

    async checkout() {
        await this.cart.reserve_seats();
        window.location.href = "/checkout_success/";
    }
}


var display = new ReservationDisplay();
await display.setup();
