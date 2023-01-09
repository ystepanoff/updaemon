$(document).ready(function() {
    let saveSourceButton = $('#saveSourceButton');
    let configureActionButtons = $('[id^="configureActionButton-"]');
    let actionModals = $('[id^="actionModal-"]');
    let addSourceButton = $('#addSourceButton');

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

    for (let actionModal of actionModals) {
        let modal = $('#' + actionModal.id)
        let parts = actionModal.id.split('-');
        let action_id = parseInt(parts[1]);
        modal.find('#cancelSaveActionIcon-' + action_id).click(() => modal.removeClass('is-active'));
        modal.find('#cancelSaveAction-' + action_id).click(() => modal.removeClass('is-active'));
        modal.find('#saveAction-' + action_id).click(function () {
            try {
                let params = modal.find('#actionParams-' + action_id).val();
                $.parseJSON(params);
                $.post(
                    "/action",
                    {
                        "source_id": $('#sourceId').val().toString(),
                        "action_id": action_id,
                        "params": params,
                    },
                    function () {
                        modal.removeClass('is-active');
                    }
                ).fail(function (xhr, status, error) {
                    alert(error);
                });
            } catch (exception) {
                alert(exception.toString());
                return;
            }
        });
    }

    for (let configureActionButton of configureActionButtons) {
        $('#' + configureActionButton.id).click(function () {
            let parts = configureActionButton.id.split('-');
            let action_id = parseInt(parts[1]);
            // TODO: params validation
            let params_config = $.parseJSON($('#actionParamsConfig-' + action_id).val());
            let modal = $('#actionModal-' + action_id)
            modal.addClass('is-active');
        });
    }

    if (addSourceButton.length) {
        addSourceButton.click(function () {
            let modal = $('#addSourceModal');
            modal.addClass('is-active');
            modal.find('#addSourceCancel').click(() => modal.removeClass('is-active'));
            modal.find('#addSourceCancelIcon').click(() => modal.removeClass('is-active'));
            modal.find('#addSourceSave').click(function () {
                let name = modal.find('#addSourceName').val();
                let description = modal.find('#addSourceDescription').val();
                let remote = modal.find('#addSourceRemote').val();
                $.post(
                    "/source",
                    {
                        "name": name,
                        "description": description,
                        "remote": remote
                    },
                    () => modal.removeClass('is-active')
                ).fail(function (xhr, status, error) {
                    alert(error);
                    modal.removeClass('is-active');
                });
            });
        });
    }
});