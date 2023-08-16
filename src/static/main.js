document.addEventListener("DOMContentLoaded", function () {
    const helloButton = document.getElementById("helloButton");
    const histData = JSON.parse('{{ hist_data | tojson | safe}}');
    alert(histData.length)

    helloButton.addEventListener("click", function () {
        // Iterate through histData and log each element
        histData.forEach(item => {
            console.log(item);
        });
        // Send an AJAX request to the Flask server
        fetch('/say_hello')
            .then(response => response.json())
            .then(data => {
                // Display the response message
                alert(data.message);
            })
            .catch(error => {
                console.error('Error:', error);
            });
    });

});
