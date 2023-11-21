document.addEventListener('alpine:init', () => {
    Alpine.store(
        'ui', {

        menu_drop: Alpine.$persist(false),
        menu_position: Alpine.$persist('menu'),
        category_modal: Alpine.$persist(false),
    },
    )
})