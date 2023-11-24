document.addEventListener('alpine:init', () => {
    Alpine.store(
        'pos', {
        selected: '',
        cart: [],
        total: 0,
        count: 0,
        init() {
            this.cart = [];
            this.total = 0;
            this.count = 0;
        },
        addToCart(p) {
            // select id, name, price from p and sotre it into product
            product = {
                id: p.id,
                name: p.name,
                image: p.image,
                price: p.price,
                quantity: 1
            }
            const index = this.findCartIndex(product);
            if (index === -1) {
                this.cart.push(product);
            } else {
                this.cart[index].quantity++;
            }
            this.total += product.price;
            this.count++;
        },
        findCartIndex(product) {
            return this.cart.findIndex(item => item.id === product.id);
        }
    },
    )
})