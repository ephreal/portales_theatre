import * as api from "./client_api.js";
import * as shopping from "./shopping_cart.js";


class Report {
    constructor() {
        this.today = new Date();
        this.today = this.today.toISOString().split("T")[0];

        this.cart = new shopping.ShoppingCart();
    }

    async group_purchased_by_play() {
        /*
         * Groups the reservations by play for a far cleaner look when
         * displaying the plays later.
         */
        var purchased = {};

        for (var i = 0; i < this.cart.purchased.length; i++) {
            var reservation = this.cart.purchased[i];
            var play = reservation.play;

            // If the play is not already in the purchased dict, add it in.
            if (play.name in purchased === false) {
                purchased[play.name] = {
                    "seats": [],
                    "total": 0,
                    "date": reservation.date.date,
                    "time": reservation.time.time
                };
            }

            // Add the parts of the play that we're interested in to the dict.
            purchased[play.name].seats.push(reservation.seat);
            purchased[play.name].total += parseInt(reservation.price);
        }
        return purchased;
    }

    async just_purchased() {
        /*
         * Gets the recently purchased items from the shopping cart and
         * displays them in the element with id=purchased
         */
        var purchased = await this.group_purchased_by_play();
        var keys = Object.keys(purchased);
        var element = document.getElementById("purchased");

        for (var i = 0; i < keys.length; i++) {
            var key = keys[i];
            element.appendChild(await this.play_element(key, purchased[key]));
            console.log(keys[i]);
        }

        // clear out the purchased items in the cart.
        await this.cart.clear_purchased();
    }

    async todays_purchases() {
        /*
         * Queries the API for all of the purchases that were made on the
         * current date.
         */

        var purchases = await api.get_reservations_by_date(this.today);
        console.log(purchases);
    }


    async play_element(name, play_json) {
        /*
         * Creates a play element that can be directly added to the document.
         */

        // Create the elements that are going to be used to display the info
        var play = document.createElement("section");
        var play_header = document.createElement("header");
        var play_name = document.createElement("p");
        var play_details = document.createElement("aside");
        var play_date = document.createElement("header");
        var cost = document.createElement("p");
        var date = document.createElement("p");
        var time = document.createElement("p");
        var seating_element = document.createElement("section");

        play.classList.add("client_purchase-reservation_play");
        play_header.classList.add("client_purchare-reservation_header");
        play_name.classList.add("client_purchase-reservation_play_name");
        play_details.classList.add("client_purchase-play_details");
        play_date.classList.add("client_purchase-play_details_header")
        seating_element.classList.add("client_purchase-seating");

        play_name.innerText = name;
        cost.innerText = `Total: \$${play_json.total}`;
        date.innerText = `Date: ${play_json.date}`
        time.innerText = `Time: ${play_json.time}`;

        play_header.append(play_name);
        play_header.append(cost);
        play_date.appendChild(date);
        play_date.appendChild(time);
        play_details.appendChild(play_date);
        play_details.append(seating_element);

        for (var i = 0; i < play_json.seats.length; i++) {
            var seat = play_json.seats[i];
            var seat_element = document.createElement("section");
            var seating = document.createElement("p");

            seat_element.classList.add("client_purchase-seat");

            seating.innerText =`row: ${seat.row} seat: ${seat.column}`;
            seat_element.appendChild(seating);
            seating_element.appendChild(seat_element);
        }


        play.appendChild(play_header);
        play.append(play_details);

        return play;
    }
}

var report = new Report();
report.just_purchased();
