function table() {
    const app = {
        menu: [],

        // init() {
        //     this.menu = JSON.parse('{{ menu_list|e }}')
        // }
    };
    return app;
}

var things = JSON.parse('{{menu | tojson}}');