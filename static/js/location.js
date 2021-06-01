// This will be the object that will contain the Vue attributes
// and be used to initialize it.
let app = {};

// Given an empty app object, initializes it filling its attributes,
// creates a Vue instance, and then initializes the Vue instance.
let init = (app) => {

    // This is the Vue data.
    app.data = {
        loc_id: 0,
        user_email: "",
        name: "",
        description: "",
        poster: "",
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
        change_filter: app.change_filter,
        apply_filter: app.apply_filter,
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
        });
    };

    // Call to the initializer.
    app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code i
init(app);
