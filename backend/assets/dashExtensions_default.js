window.dashExtensions = Object.assign({}, window.dashExtensions, {
    default: {
        function0: () => confetti({
            particleCount: 150,
            spread: 70,
            origin: {
                y: 0.6
            }
        })
    }
});