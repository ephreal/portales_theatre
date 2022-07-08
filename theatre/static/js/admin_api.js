export class APIRequest {
    constructor(api_request) {
        this.endpoint_url = `${window.location.protocol}//${window.location.hostname}:${window.location.port}/api/admin/`;
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

export class Seat {

    constructor(seat_id, price) {
        this.id = seat_id;
        this.price = price;
    }

    async to_json() {
        var json = {
            "id": this.id,
            "price": this.price
        }

        console.log(json);

        return json;
    }
}

// Frontend admin API endpoint implementation
export async function create_play(play_id, data){
    /*
     * Creates a new play.
     * data should be a json string that represents a Play object.
     *
     * Returns a JSON string containing the Play information OR an error.
     */

     var api_request = `play/`;
     var request = new APIRequest(api_request);
     return await request.post_request(data);
}

export async function get_play(play_id) {
    /*
     * Gets the play referenced by the play_id.
     *
     * Returns a JSON string containing the Play information OR an error.
     */
     var api_request = `play/${play_id}`;
     var request = new APIRequest(api_request);
     return await request.get_request();
}

export async function update_play(play_id, data) {
    /*
     * Updates the play referenced by play_id.
     *
     * The data passed in should represent a Play object.
     */
     var api_request = `play/${play_id}`;
     var request = new APIRequest(api_request);
     return await request.put_request(data);
}

export async function delete_play(play_id) {
    /*
     * Deletes the play where play.id == play_id
     *
     * Returns JSON with a success or error message
     */
     var api_request = `play/${play_id}`;
     var request = new APIRequest(api_request);
     return await request.delete_request();
}

export async function create_seat(play_id) {
    /*
     * Creates a new seat.
     *
     * Returns JSON with a success or error message.
     */
    var api_request = `seat/`;
    var request = new APIRequest(api_request);
    return await request.post_request({"play": play_id});
}

export async function get_seat(seat_id) {
    /*
     * Gets a seat identified by seat.id == seat_id
     *
     * Returns JSON with the seat information OR an error.
     */
    var api_request = `seat/${seat_id}`;
    var request = new APIRequest(api_request);
    return await request.get_request();
}

export async function update_seat(seat_id, data) {
    /*
     * Updates a seat with the information passed in.
     *
     * Returns JSON with the seat information OR an error.
     */
    var api_request = `seat/${seat_id}`;
    var request = new APIRequest(api_request);
    return await request.put_request(data);
}

export async function delete_seat(seat_id) {
    /*
     * Deletes the seat identified by seat.id == seat_id
     *
     * Returns JSON with a success or error message.
     */
     var api_request = `seat/${seat_id}`;
     var request = new APIRequest(api_request);
     return await request.delete_request();
}

export async function get_reservations(seat_id, date_id, time_id) {
    /*
     * Gets all of the seat resesrvation information for a particular play.
     */
     var api_request = `reservations/${seat_id}/${date_id}/${time_id}`;
     var request = new APIRequest(api_request);
     return await request.get_request();
}

export async function get_times(play_id) {
    /*
     * Gets all the times for a play.
     */
     var api_request = `times/${play_id}`;
     var request = new APIRequest(api_request);
     return await request.get_request();
}
