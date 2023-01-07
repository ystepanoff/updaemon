$(document).ready(function() {
    let saveSourceButton = $('#saveSourceButton');
    if (saveSourceButton.length) {
        let saveSourceFailed = $('#saveSourceFailed');
        let saveSourceSuccess = $('#saveSourceSuccess');
        saveSourceButton.click(function () {
            $.post(
                "/source",
                {
                    "id": $('#sourceId').val().toString(),
                    "name": $('#sourceName').val().toString(),
                    "description": $('#sourceDescription').val().toString(),
                    "remote": $('#sourceRemote').val().toString()
                },
                function () {
                    saveSourceSuccess.removeClass('is-hidden');
                    saveSourceSuccess.stop();
                    saveSourceSuccess.fadeTo(0, 1.0);
                    saveSourceSuccess.fadeOut(
                        5000,
                        function () {
                            saveSourceSuccess.addClass('is-hidden').fadeTo(0,1.0);
                        }
                    );
                    saveSourceFailed.addClass('is-hidden').fadeTo(0, 1.0);
                }
            ).fail(function (xhr, status, error) {
                saveSourceFailed.removeClass('is-hidden');
                saveSourceFailed.stop();
                saveSourceFailed.fadeTo(0, 1.0);
                saveSourceFailed.fadeOut(
                    5000,
                    function () {
                        saveSourceFailed.addClass('is-hidden').fadeTo(0, 1.0);
                    }
                )
            });
        });
    }
});