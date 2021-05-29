// This will be the object that will contain the Vue attributes
// and be used to initialize it.
let app = {};

// Given an empty app object, initializes it filling its attributes,
// creates a Vue instance, and then initializes the Vue instance.
let init = (app) => {

    // This is the Vue data.
    app.data = {
        upvoted: false,
        show_add_modal: false,
        location_name: "",
        location_desc: "",
        posts: [],
    };

    app.enumerate = (a) => {
        // This adds an _idx field to each element of the array.
        let k = 0;
        a.map((e) => {e._idx = k++;});
        return a;
    };

    app.set_upvote = function (status) {
        app.vue.upvoted = status;
    }

    app.set_add_modal = function () {
        app.vue.show_add_modal = !app.vue.show_add_modal;
    }

    app.reset_add_form = function () {
        app.vue.location_name = "";
        app.vue.location_desc = "";
    }

    app.add_post = function () {
        axios.post(add_location_url,
            {
                name: app.vue.location_name,
                description: app.vue.location_desc,
            }).then(function (response) {
            app.vue.posts.unshift({
                id: response.data.id,
                name: app.vue.location_name,
                description: app.vue.location_desc,
            });
            app.enumerate(app.vue.posts);
            app.reset_add_form();
            app.set_add_modal();
        });
    }

    // We form the dictionary of all methods, so we can assign them
    // to the Vue app in a single blow.
    app.methods = {
        set_upvote: app.set_upvote,
        set_add_modal: app.set_add_modal,
        add_post: app.add_post,
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
        // axios.get(load_contacts_url).then(function (response) {
        //     app.vue.rows = app.enumerate(response.data.rows);
        // });
        axios.get(get_location_url).then(function (response) {
            app.vue.posts = app.enumerate(response.data.posts);
        });
    };

    // Call to the initializer.
    app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code i
init(app);
