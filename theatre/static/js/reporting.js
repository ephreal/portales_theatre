import * as api from './reporting_api.js';


export class Report {
    constructor() {
        this.display = document.getElementById("report");
        this.start_date = document.getElementById("start_date");
        this.end_date = document.getElementById("end_date");
        this.run_report = document.getElementById("run_report");
        this.reservations = [];
        this.grouped = {};

        this.run_report.addEventListener("click", async (e) => {
            await this.report();
        });
    }

    async report() {
        // Runs the report with the options provided

        // Check to see if both dates are available
        if (! this.start_date.value || ! this.end_date.value) {
            return;
        }

        await this.clear();
        await this.reservations_by_date_range(this.start_date.value, this.end_date.value);
        await this.group_by_play();
        await this.build_report_by_play();
    }

    async clear() {
        // clears the report display
        while (this.display.firstChild) {
            this.display.removeChild(this.display.firstChild);
        }
    }

    async reservations_by_date(date) {
        // Gets a list of reservations on a certain date.
        // date must be in YYYY-MM-DD format
        this.reservations = await api.get_reservations_by_date(date);
    }

    async reservations_by_date_range(start_date, end_date) {
        // Gets a list of reservations within a specific date range
        // Dates must be in YYYY-MM-DD format

        this.reservations = await api.get_reservations_by_date_range(start_date, end_date);
        this.reservations = this.reservations['reservations'];
    }

    async group_by_play() {
        // Groups the reservations by play.

        this.grouped = {};

        for (var i = 0; i < this.reservations.length; i++) {
            var res = this.reservations[i];
            var play = res.play.name;

            if (play in this.grouped === false) {
                this.grouped[play] = {
                    "seats": [],
                    "total": 0,
                    "date": res.date.date,
                    "time": res.time.time
                }
            }

            this.grouped[play].seats.push(res.seat);
            this.grouped[play].total += res.price;
        };

    }

    async build_report_by_play() {
        // Builds the report from the grouped items.
        // Items placed into this.display

        var plays = Object.keys(this.grouped);
        plays.forEach((name, i) => {
            var play = this.grouped[name];
            var play_holder = document.createElement("section");
            var title_holder = document.createElement("section");
            var title = document.createElement("p");
            var total_seats = document.createElement("p");
            var total_price = document.createElement("p");

            play_holder.classList.add("admin_report-play_holder");
            var datetime_holder = document.createElement("section");
            var datetime = document.createElement("p");

            var seating_holder = document.createElement("section");
            seating_holder.classList.add("admin_report-seating_holder");

            title_holder.classList.add("admin_report-play_name")
            title_holder.appendChild(title)
            title_holder.appendChild(datetime_holder);
            title.innerText = name;

            datetime_holder.classList.add("admin_report-datetime_holder");
            datetime_holder.appendChild(datetime);
            datetime.innerText = `Date: ${play.date} Time: ${play.time}`

            title_holder.append(datetime_holder);

            for (var i = 0; i < play.seats.length; i++) {
                var seat = document.createElement("p");
                seat.innerText = `Row ${play.seats[i].row} Seat: ${play.seats[i].column}`;
                seating_holder.appendChild(seat);
            }

            play_holder.appendChild(title_holder);
            play_holder.appendChild(seating_holder);
            this.display.appendChild(play_holder);
        });

    }
}


var report = new Report();
