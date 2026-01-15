// static/js/notifications.js
document.addEventListener('DOMContentLoaded', () => {
    const flash = document.getElementById("flash-message");
    
    // We check if the variable exists and has data
    if (typeof flashedMessages !== 'undefined' && flashedMessages.length > 0) {
        const [category, message] = flashedMessages[0];
        
        flash.style.display = "block";
        flash.innerText = message;
        flash.className = `flash-message ${category}`;
        
        setTimeout(() => { 
            flash.style.display = "none"; 
        }, 3000);
    }
});