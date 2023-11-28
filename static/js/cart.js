function initApp() {
    const app = {
        selected: '',
        cart: [],
        count: 0,
        order: {},
        init() {
            this.cart = [];
            this.order = {
                order_id: ULID.ulid(),
                restaurant_id: '',
                table_number: '',
                status: 'pending',
                order_type: 'dine-in',
                payment_status: 'pending',
                total: 0,
                coupon_code: '',
                note: '',
                items: []
            };
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
            this.count++;
        },
        findCartIndex(product) {
            return this.cart.findIndex(item => item.id === product.id);
        },
        addQuantity(product) {
            const index = this.findCartIndex(product);
            this.cart[index].quantity++;
            this.count++;
        },
        removeQuantity(product) {
            const index = this.findCartIndex(product);
            if (this.cart[index].quantity > 1) {
                this.cart[index].quantity--;
                this.count--;
            }
        },
        getTotal() {
            let total = 0;
            this.cart.forEach(item => {
                total += item.price * item.quantity;
            });
            return total;
        },
        removeItem(product) {
            const index = this.findCartIndex(product);
            this.count -= this.cart[index].quantity;
            this.cart.splice(index, 1);
        },
        formatMoney(money) {
            return money.toLocaleString('vi', { style: 'currency', currency: 'VND' });
        },
        checkout() {
            this.order.total = this.getTotal();
            this.order['items'] = this.cart.forEach(item => {
                return {
                    order_id: this.order.order_id,
                    menu_item_id: item.id,
                    quantity: item.quantity,
                    price: item.price,
                }
            });
            console.log(this.order);
        }
    };
    return app;
}