document.addEventListener('DOMContentLoaded', function () {
    // Star animation
    const canvas = document.getElementById("spaceCanvas");
    const ctx = canvas.getContext("2d");
    let stars = [];
    const numStars = 200;

    function resizeCanvas() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        if (!stars.length) createStars();
    }

    function createStars() {
        stars = Array.from({ length: numStars }, () => ({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            speed: Math.random() * 2 + 0.5,
            size: Math.random() * 2
        }));
    }

    function updateStars() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = "rgba(255, 255, 255, 0.8)";
        stars.forEach(star => {
            ctx.beginPath();
            ctx.arc(star.x, star.y, star.size, 0, Math.PI * 2);
            ctx.fill();
            star.y -= star.speed;
            if (star.y < 0) {
                star.y = canvas.height;
                star.x = Math.random() * canvas.width;
            }
        });
        requestAnimationFrame(updateStars);
    }

    window.addEventListener("resize", resizeCanvas);
    resizeCanvas();
    updateStars();

    // Buttons
    const loginButton = document.getElementById("login-btn");
    const signInBtn = document.getElementById("sign-up-btn");
    const organizerBtn = document.getElementById("organizer-btn");

    // Button Actions
    loginButton.addEventListener('click', function () {
        location.href = "/login";
    });

    signInBtn.addEventListener('click', function () {
        location.href = "/signup";"/dashboard";
    });

    organizerBtn.addEventListener('click', function () {
        location.href = "/orglogin"; // Or "/organizers" if that's your route
    });
});
