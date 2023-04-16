if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('static/assets/js/PWA/sw.js').then(registration => {
        // console.log('SW Registersssswsed');
        // console.log(registration);
    }).catch(error => {
        // console.log('SW Registration Failed');
        // console.log(error);
    });
}