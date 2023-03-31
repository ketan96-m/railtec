// Define a click event handler for the button
$('#new-window-btn').click(function() {
    // Get the URL of the new window from the data-href attribute
    var url = $(this).data('href');

    // Open the new window with the desired URL
    window.open(url, '_blank');

    // Prevent the default behavior of the button (i.e. submitting a form)
    return false;
});