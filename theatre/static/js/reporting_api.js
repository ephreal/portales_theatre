export class APIRequest {
    constructor(api_request) {
        this.endpoint_url = `${window.location.protocol}//${window.location.hostname}:${window.location.port}/api/report/`;
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


export async function get_reservations_by_date(date) {
    // Queries the API to get the reports for a specific date.
    var api_request = `date/${date}`;
    var request = new APIRequest(api_request);
    return await request.get_request();
}


export async function get_reservations_by_date_range(start_date, end_date) {
    // Queries the API to get reservations within a specific date range
    var api_request = `date_range/${start_date}/${end_date}`;
    var request = new APIRequest(api_request);
    return await request.get_request();
}
