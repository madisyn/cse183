// This will be the object that will contain the Vue attributes
// and be used to initialize it.
let app = {};

// Given an empty app object, initializes it filling its attributes,
// creates a Vue instance, and then initializes the Vue instance.
let init = (app) => {

    // This is the Vue data.
    app.data = {
        user_email: "",
        show_add_modal: false,
        location_name: "",
        location_desc: "",
        cry_rating: 0,
        atmos_rating: 0,
        noise_rating: 0,
        ppl_rating: 0,
        review_content: "",
        posts: [],
        filter: "top",
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
        app.vue.location_name = "";
        app.vue.location_desc = "";
        app.vue.cry_rating = 0;
        app.vue.atmos_rating = 0;
        app.vue.noise_rating = 0;
        app.vue.ppl_rating = 0;
        app.vue.review_content = "";
    }

    app.add_post = function () {
        axios.post(add_location_url,
            {
                name: app.vue.location_name,
                description: app.vue.location_desc,
            }).then(function (loc_response) {

            // add review
            axios.post(add_review_url,
                {
                    location: loc_response.data.id,
                    cry: app.vue.cry_rating,
                    atmosphere: app.vue.atmos_rating,
                    noise: app.vue.noise_rating,
                    people: app.vue.ppl_rating,
                    comment: app.vue.review_content,
                }).then(function (response) {

                app.vue.posts.unshift({
                    id: loc_response.data.id,
                    name: app.vue.location_name,
                    description: app.vue.location_desc,
                    email: app.vue.user_email,
                    review_count: response.data.updated.review_count,
                    avg_rating: response.data.updated.avg_rating,
                    avg_noise: response.data.updated.avg_noise,
                    avg_people: response.data.updated.avg_people,
                    avg_atmosphere: response.data.updated.avg_atmosphere,
                    avg_cry: response.data.updated.avg_cry,
                    tags: response.data.updated.tags,
                });
                app.apply_filter();
                app.enumerate(app.vue.posts);
                
                app.reset_add_form();
                app.set_add_modal();
            });
        });
    }

    app.delete_post = function (post_idx) {
        let id = app.vue.posts[post_idx].id;
        axios.get(delete_location_url, {params: {id: id}}).then(function (response) {
            for (let i = 0; i < app.vue.posts.length; i++) {
                if (app.vue.posts[i].id === id) {
                    app.vue.posts.splice(i, 1);
                    app.enumerate(app.vue.posts);
                    break;
                }
            }
        });
    }

    app.open_location = function (object, post_id) {
        object.location.href = location_url + '/' + post_id;
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
        add_post: app.add_post,
        delete_post: app.delete_post,
        open_location: app.open_location,
        change_filter: app.change_filter,
        apply_filter: app.apply_filter,
    };

    // This creates the Vue instance.
    app.vue = new Vue({
        el: "#vue-target",
        data: app.data,
        methods: app.methods
    });

    // And this initializes it.
    // Generally, this will be a network call to the server to
    // load the data.
    // For the moment, we 'load' the data from a string.
    app.init = () => {
        axios.get(get_email_url).then(function (response) {
            app.vue.user_email = response.data.email;
        })
        axios.get(get_locations_url).then(function (response) {
            app.vue.posts = app.enumerate(response.data.posts);
            app.apply_filter();
        });
    };

    // Call to the initializer.
    app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code i
init(app);
