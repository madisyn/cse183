// This will be the object that will contain the Vue attributes
// and be used to initialize it.
let app = {};

// Given an empty app object, initializes it filling its attributes,
// creates a Vue instance, and then initializes the Vue instance.
let init = (app) => {

    // This is the Vue data.
    app.data = {
        loc_id: null,
        user_email: "",
        name: "",
        description: "",
        poster: "",
        review_count: 0,
        avg_rating: 0,
        avg_noise: 0,
        avg_people: 0,
        avg_atmosphere: 0,
        avg_cry: 0,
        tags: [],
        show_add_modal: false,
        cry_rating: 0,
        atmos_rating: 0,
        noise_rating: 0,
        ppl_rating: 0,
        review_content: "",
        reviews: [],
        filter: "top",
        upvoted: true,
    };

    app.enumerate = (a) => {
        // This adds an _idx field to each element of the array.
        let k = 0;
        a.map((e) => {e._idx = k++;});
        return a;
    };

    app.set_add_modal = function () {
        app.vue.show_add_modal = !app.vue.show_add_modal;
        if (!app.vue.show_add_modal) {
            app.reset_add_form();
        }
    }

    app.reset_add_form = function () {
        app.vue.cry_rating = 0;
        app.vue.atmos_rating = 0;
        app.vue.noise_rating = 0;
        app.vue.ppl_rating = 0;
        app.vue.review_content = "";
    }

    app.add_review = function () {
        axios.post(add_review_url,
            {
                location: app.vue.loc_id,
                cry: app.vue.cry_rating,
                atmosphere: app.vue.atmos_rating,
                noise: app.vue.noise_rating,
                people: app.vue.ppl_rating,
                comment: app.vue.review_content,
            }).then(function (response) {
            app.vue.reviews.unshift({
                id: response.data.id,
                cry_rating: app.vue.cry_rating,
                atmosphere_rating: app.vue.atmos_rating,
                noise_rating: app.vue.noise_rating,
                people_rating: app.vue.ppl_rating,
                comment: app.vue.review_content,
                helpful_count: 0,
                date_posted: response.data.date_posted,
                username: response.data.username,
            });
            // update averages
            app.vue.review_count = response.data.updated.review_count;
            app.vue.avg_rating = response.data.updated.avg_rating;
            app.vue.avg_noise = response.data.updated.avg_noise;
            app.vue.avg_people = response.data.updated.avg_people;
            app.vue.avg_atmosphere = response.data.updated.avg_atmosphere;
            app.vue.avg_cry = response.data.updated.avg_cry;
            app.vue.tags = response.data.updated.tags;

            app.apply_filter();
            app.enumerate(app.vue.reviews);
            app.reset_add_form();
            app.set_add_modal();
        });
    }

    app.delete_review = function (review_idx) {
        let id = app.vue.reviews[review_idx].id;
        axios.get(delete_review_url, {params: {id: id, location: loc_id}}).then(function (response) {
            for (let i = 0; i < app.vue.reviews.length; i++) {
                if (app.vue.reviews[i].id === id) {
                    app.vue.reviews.splice(i, 1);
                    app.enumerate(app.vue.reviews);
                    break;
                }
            }
            // update averages
            app.vue.review_count = response.data.updated.review_count;
            app.vue.avg_rating = response.data.updated.avg_rating;
            app.vue.avg_noise = response.data.updated.avg_noise;
            app.vue.avg_people = response.data.updated.avg_people;
            app.vue.avg_atmosphere = response.data.updated.avg_atmosphere;
            app.vue.avg_cry = response.data.updated.avg_cry;
            app.vue.tags = response.data.updated.tags;
        });
    }

    app.parse_date = function (datetime) {
        // format: YYYY-MM-DDTHH:MM:SS.mmmmmm
        const year = datetime.substring(2, 4);
        const month = datetime.substring(5, 7);
        const day = datetime.substring(8, 10);
        return month + "/" + day + "/" + year;
    }

    app.change_filter = function (new_filter) {
        app.vue.filter = new_filter;
        app.apply_filter();
    }

    app.apply_filter = function () {
        // TODO
    }

    // We form the dictionary of all methods, so we can assign them
    // to the Vue app in a single blow.
    app.methods = {
        set_add_modal: app.set_add_modal,
        change_filter: app.change_filter,
        apply_filter: app.apply_filter,
        add_review: app.add_review,
        delete_review: app.delete_review,
        parse_date: app.parse_date,
    };

    // This creates the Vue instance.
    app.vue = new Vue({
        el: "#vue-location",
        data: app.data,
        methods: app.methods
    });

    // And this initializes it.
    // Generally, this will be a network call to the server to
    // load the data.
    // For the moment, we 'load' the data from a string.
    app.init = () => {
        app.vue.loc_id = loc_id;
        axios.get(get_email_url).then(function (response) {
            app.vue.user_email = response.data.email;
        });
        axios.get(get_location_url, {params: {loc_id: loc_id}}).then(function (response) {
            app.vue.name = response.data.location.name;
            app.vue.description = response.data.location.description;
            app.vue.poster = response.data.location.email;
            app.vue.review_count = response.data.location.review_count;
            app.vue.avg_rating = response.data.location.avg_rating;
            app.vue.avg_noise = response.data.location.avg_noise;
            app.vue.avg_people = response.data.location.avg_people;
            app.vue.avg_atmosphere = response.data.location.avg_atmosphere;
            app.vue.avg_cry = response.data.location.avg_cry;
            app.vue.tags = response.data.location.tags;
        });
        axios.get(get_reviews_url, {params: {loc_id: loc_id}}).then(function (response) {
            app.vue.reviews = app.enumerate(response.data.reviews);
            app.apply_filter();
        });
    };

    // Call to the initializer.
    app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code i
init(app);
