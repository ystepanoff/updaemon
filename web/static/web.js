$(document).ready(function() {
    let saveSourceButton = $('#saveSourceButton');
    let addSourceButton = $('#addSourceButton');
    let deleteSourceButtons = $('[id^="deleteSourceButton-"]');
    let configureActionButtons = $('[id^="configureActionButton-"]');
    let actionModals = $('[id^="actionModal-"]');
    let addActionButton = $('#addActionButton');

    if (saveSourceButton.length) {
        let saveSourceFailed = $('#saveSourceFailed');
        let saveSourceSuccess = $('#saveSourceSuccess');
        saveSourceButton.click(function () {
            $.post(
                "/source",
                {
                    "source_id": $('#sourceId').val().toString(),
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
        let source_action_id = parseInt(parts[1]);
        modal.find('#cancelSaveActionIcon-' + source_action_id).click(() => modal.removeClass('is-active'));
        modal.find('#cancelSaveAction-' + source_action_id).click(() => modal.removeClass('is-active'));
        modal.find('#saveAction-' + source_action_id).click(function () {
            try {
                let params = modal.find('#actionParams-' + source_action_id).val();
                $.parseJSON(params);
                $.post(
                    "/action",
                    {
                        "source_id": $('#sourceId').val().toString(),
                        "action_id": modal.find('#actionId').val(),
                        "source_action_id": source_action_id,
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
            }
        });
    }

    for (let configureActionButton of configureActionButtons) {
        $('#' + configureActionButton.id).click(function () {
            let parts = configureActionButton.id.split('-');
            let source_action_id = parseInt(parts[1]);
            // TODO: params validation
            let params_config = $.parseJSON($('#actionParamsConfig-' + source_action_id).val());
            let modal = $('#actionModal-' + source_action_id)
            modal.addClass('is-active');
        });
    }

    if (addSourceButton.length) {
        let modal = $('#addSourceModal');
        modal.find('#addSourceCancel').click(() => modal.removeClass('is-active'));
        modal.find('#addSourceCancelIcon').click(() => modal.removeClass('is-active'));
        addSourceButton.click(function () {
            modal.addClass('is-active');
        });
        modal.find('#addSourceSave').click(function () {
            let name = modal.find('#addSourceName').val();
            let description = modal.find('#addSourceDescription').val();
            let remote = modal.find('#addSourceRemote').val();
            $.post(
                "/source",
                {
                    "name": name,
                    "description": description,
                    "remote": remote,
                },
                () => modal.removeClass('is-active')
            ).fail(function (xhr, status, error) {
                alert(error);
                modal.removeClass('is-active');
            });
        });
    }

    for (let deleteSourceButton of deleteSourceButtons) {
        $('#' + deleteSourceButton.id).click(function () {
            if (confirm("Do you want to delete this source?")) {
                let parts = deleteSourceButton.id.split('-');
                let source_id = parseInt(parts[1]);
                $.post(
                    "/source",
                    {
                        "source_id": source_id,
                        "delete": true
                    },
                    () => location.reload()
                ).fail(function (xhr, status, error) {
                    alert(error);
                });
            }
        });
    }

    if (addActionButton.length) {
        let modal = $('#addActionModal');
        modal.find('#addActionCancel').click(() => modal.removeClass('is-active'));
        modal.find('#addActionCancelIcon').click(() => modal.removeClass('is-active'));
        addActionButton.click(function () {
            modal.addClass('is-active');
        });
        modal.find('#addActionSave').click(function () {
            let baseClassId = parseInt(modal.find('#addActionBaseClass').val());
            let params = modal.find('#addActionParams').val();
            try {
                $.parseJSON(params);
                $.post(
                    "/action",
                    {
                        "source_id": $('#sourceId').val().toString(),
                        "action_id": baseClassId,
                        "params": params
                    },
                    () => modal.removeClass('is-active')
                ).fail(function (xhr, status, error) {
                    alert(error);
                    modal.removeClass('is-active');
                });
            } catch (exception) {
                alert(exception.toString());
            }
        });
    }
});