import * as api from "./client_api.js";
import * as shopping from "./shopping_cart.js";

/* Bind the event handler to each and every seat */
let seats = document.getElementsByClassName("seat");
seats = Array.from(seats);
let cart = new shopping.ShoppingCart();

for (var i = 0; i < seats.length; i++) {
    let seat = seats[i];
    seat.addEventListener("click", async (event) => {
        await seat_clicked(seat, event);
    });
    let seat_id = seat.getAttribute("seat");
    let date_id = seat.getAttribute("date");
    let time_id = seat.getAttribute("time");
    let in_cart = await cart.check(seat_id, date_id, time_id);

    if (in_cart >= 0 && ! seat.classList.contains("seat-reserved")) {
        seat.classList.add("seat-in_cart");
    }
}

async function seat_clicked(seat, event) {
    /*
     * Ran when a user clicks on a seat.
     *
     * Queries the server to get the seat data that matches this time.
     * once the information has been returned, creates an element next to the
     * location where the mouse was clicked that is populated with the info.
     */
     let id = seat.getAttribute("seat");
     let date = seat.getAttribute("date");
     let time = seat.getAttribute("time");
     let x_pos = event.clientX;
     let y_pos = event.clientY;
     let reserved = seat.classList.contains("seat-reserved");
     let in_cart = seat.classList.contains("seat-in_cart");
     let play = document.getElementById("play_id").getAttribute("play");

     if ((! reserved) && in_cart) {
         // var removal = await api.remove_reservation(id, date, time);
         var removal = await cart.remove(id, date, time);
         if (! removal.error ) {
             seat.classList.remove("seat-in_cart");
             seat.classList.add("seat-available");
         }
     }
     else if (! reserved) {
         var reservation = cart.add(id, date, time);
         if (! reservation.error) {
             seat.classList.add("seat-in_cart");
             seat.classList.remove("seat-available");
         }
     }

}
