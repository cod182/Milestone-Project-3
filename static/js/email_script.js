const submitButton = document.getElementById('contact-submit');
const cName = document.getElementById('contact-name');
const email = document.getElementById('contact-email');
const message = document.getElementById('contact-message');

// Code adapted from eamil lesson from code instutite
function sendEmail(contactForm) {
    emailjs.send('gmail','codie',{
        "from_name": contactForm.name.value,
        "from_email": contactForm.email.value,
        "reason": contactForm.reason.value,
        "message": contactForm.message.value
    })
    .then(
        function(response) {
            console.log('SUCCESS',response);
            document.getElementById('message-status').innerHTML =`<span class='green bold message-status'><em>Message Sent!</em> <i class="green fas fa-check-circle"></i></span>`;
            submitButton.classList.remove('btn-blue');
            submitButton.classList.add('btn-success');
            submitButton.disabled = true;
            setTimeout(function(){ 
                document.getElementById('contact-modal-close').click();
                submitButton.disabled = false;
                document.getElementById('message-status').innerHTML =``;
                submitButton.classList.remove('btn-success');
                submitButton.classList.add('btn-blue');
                cName.value = '';
                email.value = '';
                message.value = '';
            }, 2000);
        },
        function(error) {
            console.log('FAILED', error);
            document.getElementById('message-status').innerHTML =`<span class='red bold'><em>Error! Please try again.</em></span>`;
        });
    return false;
}