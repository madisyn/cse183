// This will be the object that will contain the Vue attributes
// and be used to initialize it.
let app = {};

// Given an empty app object, initializes it filling its attributes,
// creates a Vue instance, and then initializes the Vue instance.
let init = (app) => {

    // This is the Vue data.
    app.data = {
        add_user_name: "",
    };

    app.enumerate = (a) => {
        // This adds an _idx field to each element of the array.
        let k = 0;
        a.map((e) => {e._idx = k++;});
        return a;
    };

    app.add_username = function (object) {
        axios.post(add_username_url,
            {
                username: app.vue.add_user_name
            }).then(function (response) {
                object.location.href = home_url;
                app.reset_form();
            })
            
    };

    app.reset_form = function () {
        app.vue.add_user_name = "";
    };

    // We form the dictionary of all methods, so we can assign them
    // to the Vue app in a single blow.
    app.methods = {
        add_username: app.add_username,
    };

    // This creates the Vue instance.
    app.vue = new Vue({
        el: "#vue-signup",
        data: app.data,
        methods: app.methods
    });

    // And this initializes it.
    // Generally, this will be a network call to the server to
    // load the data.
    // For the moment, we 'load' the data from a string.
    app.init = () => {
        // nothing to init
    };

    // Call to the initializer.
    app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code i
init(app);
