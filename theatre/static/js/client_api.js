/*
 * This is the implementation of the client API in javascript.
 * This module can be imported and used in any JS that must communicate with
 * the client API.
 */


export class APIRequest {
    constructor(api_request) {
        this.endpoint_url = `${window.location.protocol}//${window.location.hostname}:${window.location.port}/api/client/`;
        this.headers = {
            'Content-Type': 'application/json'
        };
        this.response = {}
        this.api_request = this.endpoint_url + api_request;
    }
    async get_request() {
        this.response = await fetch(this.api_request, {
            method: "GET",
            mode: "cors",
            cache: "no-cache",
            credentials: "same-origin",
            headers: this.headers,
            redirect: "follow"
            // body: JSON.stringify(data)
        });
        return this.response.json();
    }
    async put_request(data={}) {
        this.response = await fetch(this.api_request, {
            method: "PUT",
            mode: "cors",
            cache: "no-cache",
            credentials: "same-origin",
            headers: this.headers,
            redirect: "follow",
            body: JSON.stringify(data)
        });
        return this.response.json();
    }
    async post_request(data={}) {
        this.response = await fetch(this.api_request, {
            method: "POST",
            mode: "cors",
            cache: "no-cache",
            credentials: "same-origin",
            headers: this.headers,
            redirect: "follow",
            body: JSON.stringify(data)
        });
        return this.response.json();
    }
    async delete_request(data={}) {
        this.response = await fetch(this.api_request, {
            method: "DELETE",
            mode: "cors",
            cache: "no-cache",
            credentials: "same-origin",
            headers: this.headers,
            redirect: "follow",
            body: JSON.stringify(data)
        });
        return this.response.json();
    }
}


// Client API endpoint implementation

 export async function get_seat(seat_id) {
    /*
     * Uses a GET request to request the information for the seat id.
     *
     * Returns a JSON string with all the data returned from the server.
     */
    var api_request = `seat/${seat_id}`;
    var request = new APIRequest(api_request);
    return await request.get_request();
 }

export async function get_play(play_id) {
    /*
     * Uses a GET request to request the information for the play with
     * id==play_id
     *
     * Returns a JSON string containing all the data from the server
     */

    var api_request = `play/${play_id}`;
    var request = new APIRequest(api_request);
    return await request.get_request();
}

export async function make_reservation(seat_id, date_id, time_id) {
    /*
     * Reserves a seat for a specified date and time.
     */
    var api_request = `reservation/`;
    var data = {
        "seat_id": seat_id,
        "date_id": date_id,
        "time_id": time_id
    };
    var request = new APIRequest(api_request);
    return await request.post_request(data);
}

export async function remove_reservation(seat_id, date_id, time_id) {
    /*
     * Removes a reservation. If the user sending this request did not make
     * the reservation, no changes are made.
     */
    var api_request = `reservation/`;
    var data = {
        "seat_id": seat_id,
        "date_id": date_id,
        "time_id": time_id
    };
    var request = new APIRequest(api_request);
    return await request.delete_request(data);
}

export async function get_reservations(play_id, date_id, time_id) {
    /*
     * Gets all of the seat resesrvation information for a particular play.
     */
    var api_request = `reservations/${play_id}/${date_id}/${time_id}`;
    var request = new APIRequest(api_request);
    return await request.get_request();
}

export async function get_reservations_by_date(date) {
    /*
     * Gets all of the reservations of the currently logged in user for the
     * specified date.
     */
    var api_request = `reservations/by_date/${date}`;
    var request = new APIRequest(api_request);
    return await request.get_request();
}

export async function check_reservation(seat_id, date_id, time_id) {
    /*
     * Gets all of the seat resesrvation information for a particular play.
     */
    var api_request = `reservation/${seat_id}/${date_id}/${time_id}`;
    var request = new APIRequest(api_request);
    return await request.get_request();
}

export async function get_date(date_id) {
    /*
     * Gets all of the seat resesrvation information for a particular play.
     */
    var api_request = `date/${date_id}`;
    var request = new APIRequest(api_request);
    return await request.get_request();
}

export async function get_time(time_id) {
    /*
     * Gets all of the seat resesrvation information for a particular play.
     */
    var api_request = `time/${time_id}`;
    var request = new APIRequest(api_request);
    return await request.get_request();
}
