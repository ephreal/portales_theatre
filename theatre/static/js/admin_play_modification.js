import * as api from './admin_api.js';


/* Bind the event handler to each and every seat */
let seats = document.getElementsByClassName("seat");
let reserved = document.getElementById("reserved_amount");
let reserved_counter = 0;

let update_button = document.getElementById("update_price");
update_button.addEventListener("click", async (event) => {
    await update_seats();
});

Array.from(seats).forEach((seat, i) => {
    seat.addEventListener("click", async (event) => {
        await seat_selected(seat, event);
    });

    if (seat.classList.contains("seat-reserved")) {
        reserved_counter += 1;
    }
});

reserved.innerHTML = reserved_counter;

async function seat_selected(seat, event) {
    /*
     * Modifies the elements on the HMTL. For example, when a seat is selected,
     * it will update the total amount of selected seats and the total price
     * of all the selected seats.
     *
     * Parameters:
     *
     * seat: HTML Element
     */
    var id = seat.getAttribute("seat");
    var price = parseInt(seat.getAttribute("price"));

    if (seat.classList.contains("seat-selected")) {
        seat.classList.remove("seat-selected");
        await modify_total_selected(-1);
        await modify_price(price * -1);
    }
    else {
        seat.classList.add("seat-selected");
        await modify_total_selected(1);
        await modify_price(price);
    }
}

async function modify_total_selected(amt) {
    /*
     * Modifies the total amount of selected items on the page.
     * Positive numbers increment while negative numbers decrement.
     *
     * Parameters:
     *
     * amt: Integer
     */
    var selected = document.getElementById("selected_amount");
    var selected_amt = parseInt(selected.innerHTML);
    selected_amt += amt;
    selected.textContent = selected_amt;
}

async function modify_price(amt) {
    /*
     * Modifies the total price of all of the selected seats on the page.
     * Positive numbers increment while negative numbers decrement.
     *
     * Parameters:
     *
     * amt: Integer
     */
    var price = document.getElementById("total_price");
    var price_amt = parseInt(price.innerHTML);
    price_amt += amt;
    price.textContent = price_amt;
}

async function update_seats() {
    /*
     * Creates a seat object and sends the data to the update_seat() function
     * of the api.
     *
     * If the updates are successful, it will update the HTML elements on the
     * page to mirror the data.
     */

    var seat_price = document.getElementById("seat-price").value;
    var seat_price = parseInt(seat_price);

    var selected_seats = document.getElementsByClassName("seat-selected");

    var id;
    var price;

    for (var seat of selected_seats) {
        id = seat.getAttribute("seat");
        price = parseInt(seat.getAttribute("price"));

        var seat_json = new api.Seat(id, seat_price);
        seat_json = await seat_json.to_json();
        seat_json = await api.update_seat(id, seat_json);

        seat.setAttribute("price", seat_price);
        await modify_price(-1 * price);
        await modify_price(seat_price);
    }
}
