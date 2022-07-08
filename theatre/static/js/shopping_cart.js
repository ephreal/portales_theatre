import * as api from "./client_api.js";

export class ShoppingCart {
    /*
     * A shopping cart needs to be acapable of the following actions.
     *
     * 1) Add items to the cart (cart.add(item))
     * 2) Remove items from the cart (cart.remove(seat_id, date_id, time_id))
     * 3) Provide the amount of items in the cart
     * 4) Provide the items in the cart
     *
     * Since a shopping cart will only be used to reserve seats, the shopping
     * cart will only be used to hold reservations.
     */
    constructor(contents, purchased) {
        // Contents may not always be initialized properly. Ensure that this
        // is a list if nothing is passed in.
        this.shopping_cart_counter = document.getElementById("shopping_cart_counter");
        if (contents && purchased) {
            this.contents = contents;
            this.purchased = purchased;
        }
        else {
            this.load();
        }
        this.checkout_url = "/checkout/";
    }

    async display_contents() {
        console.log("contents\n========");
        console.log(this.contents);
        console.log("purchased\n=========");
        console.log(this.purchased);
    }

    async check(seat_id, date_id, time_id) {
        /*
         * Checks the shopping cart to see if it contains a reservation for a
         * seat.
         */
        for (var i = 0; i < this.contents.length; i++) {
            if (this.contents[i].seat === seat_id &&
                this.contents[i].date === date_id &&
                this.contents[i].time === time_id) {

                    return i;
            }
        }
        return -1;
    }

    load() {
        /*
         * Loads the contents of the shopping cart local storage into the cart.
         */

         // Load the cart contents from local storage if it exists
        if (localStorage['cart_contents']){
            this.contents = JSON.parse(localStorage.getItem('cart_contents'));
        }
        else {
            this.contents = [];
        }

        // Set the shopping car counter
        this.shopping_cart_counter.textContent = this.contents.length;

        // Load the purchased items from local storage if they exist
        if (localStorage['cart_purchased']) {
            this.purchased = JSON.parse(localStorage.getItem('cart_purchased'));
        }
        else {
            this.purchased = [];
        }
    }

    async store() {
        /*
         * Stores the contents of the cart to the local storage
         */
        localStorage.setItem('cart_contents', JSON.stringify(this.contents));
        localStorage.setItem('cart_purchased', JSON.stringify(this.purchased));
    }

    async add(seat_id, date_id, time_id) {
        /*
         * Adds a reservation to the shopping cart.
         * If the seat has already been reserved by anyone else (including the
         * current user), this does nothing.
         *
         * Parameters:
         *     seat_id: int
         *     date_id: int
         *     time_id: int
         *
         * Returns:
         *     Reservation or Error
         */
         var reservation = await api.check_reservation(seat_id, date_id, time_id);

         // Check if there is an error with the data OR if the reservation
         // already exists
         if (! (reservation.error === "Reservation not found")) {
             return reservation;
         }

         let res = {
             "seat": seat_id,
             "date": date_id,
             "time": time_id
         }

         this.contents.push(res);
         await this.store();
         this.shopping_cart_counter.textContent = parseInt(this.shopping_cart_counter.innerHTML) + 1;
         return reservation;
    }

    async remove(seat_id, date_id, time_id) {
        /*
         * Removes a particular reservation from the shopping cart.
         * If the seat has already been removed, this does nothing.
         *
         * Parameters:
         *     seat_id: int
         *     date_id: int
         *     time_id: int
         *
         * Returns:
         *     Success or Error
         */

        var index = await this.check(seat_id, date_id, time_id);
        if (index === -1) {
            return {"error": "Item did not exist in shopping cart contents."};
        }

        this.contents.splice(index, 1);
        await this.store();
        this.shopping_cart_counter.textContent = parseInt(this.shopping_cart_counter.innerHTML) - 1;
        return index;
    }

    async report() {
        /*
         * Creates a report from the reservations in the shopping cart.
         *
         * Parameters:
         *     None
         *
         * Returns:
         *     Report {res1: {cost, name}, res2:....}
         */
         var customer_report = {}
    }

    async reserve_seats() {
        /*
         * Reserves the seats in this.contents.
         */
        for (var i = 0; i < this.contents.length; i++) {
            var seat_id = this.contents[i]['seat']
            var date_id = this.contents[i]['date']
            var time_id = this.contents[i]['time']

            var reservation = await api.make_reservation(seat_id, date_id, time_id);

            if (reservation.error) {
                console.log(reservation.error);
            }
            else {
                this.purchased.push(reservation);
            }
        }

        // Clear the cart since items have ether been purchased OR they are unable to be reserved
        await this.store();
        this.clear();
    }

    async clear() {
        this.contents = [];
        localStorage.setItem('cart_contents', JSON.stringify([]));
        this.shopping_cart_counter.textContent = 0;
    }

    async clear_purchased() {
        this.purchased = [];
        localStorage.setItem('cart_purchased', JSON.stringify([]));
    }
}
